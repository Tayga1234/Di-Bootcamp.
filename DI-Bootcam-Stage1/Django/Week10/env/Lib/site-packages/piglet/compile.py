# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
piglet.compile - compile the intermediate source representation (as output by
:func:`piglet.compilexml.compile`) into python byte code.
"""

from ast import (
    AST,
    Assign,
    Attribute,
    Call,
    Constant,
    Dict,
    ExceptHandler,
    Expr,
    If,
    FunctionDef,
    ImportFrom,
    Index,
    List,
    Load,
    Module,
    Name,
    Param,
    Pass,
    Store,
    Subscript,
    Try,
    Yield,
    YieldFrom,
    alias,
    arguments,
    keyword,
)
from typing import Sequence

try:
    from ast import arg
except ImportError:
    arg = None

from collections import defaultdict
from contextlib import contextmanager
from functools import wraps
from itertools import chain, count
import hashlib
import io
import re
import sys
import types

import astunparse

from piglet import intermediate as im
from piglet import interpolate
from piglet.astutil import (
    add_arg_default,
    add_kwarg,
    add_locations,
    astwalk,
    get_comparison,
    make_arg,
    make_kwarg,
    parse_and_strip,
    LoadAttribute,
    LoadName,
    StoreName,
)
from piglet.exceptions import PigletParseError, PigletError

# Starting from python 3.8, Num, Str and a few other symbols are
# deprecated in favour of Constant. The semantics are slightly different
# though, so we can't simply alias the old symbol names. We also need to
# set various attributes ('n' for a Num, 's' for a str) else we
# get errors in astunparse.
#
# Note also that the order of keyword arguments to ast.Constant is also
# important to get right.
#
# See:
# - https://github.com/simonpercivall/astunparse/issues/43
# - https://bugs.python.org/issue32892


def Num(n):
    return Constant(n, s=None, n=n, kind=None)


def Str(s):
    return Constant(s, n=None, s=s, kind=None)


try:
    import builtins
except ImportError:
    import __builtin__ as builtins

builtin_names = set(builtins.__dict__) | {"True", "False"}


if hasattr(Exception(), "with_traceback"):

    def reraise(exc_type, exc_inst, tb):
        raise exc_inst.with_traceback(tb)


else:
    exec("def reraise(exc_type, exc_inst, tb):\n" "    raise exc_type, exc_inst, tb\n")

is_whitespace = re.compile(r"^\s*$", re.S).match


def annotate_errors(fn):
    """
    Wrapper for that catches compile time errors and annotates them with the
    correct line number
    """

    @wraps(fn)
    def annotate_errors(*args, **kwargs):
        try:
            try:
                return fn(*args, **kwargs)
            except SyntaxError as se:
                raise PigletParseError(repr(se))
        except PigletError as e:
            srcnode = next(
                (item for item in iter(args) if isinstance(item, im.IntermediateNode)),
                None,
            )

            if srcnode is not None and srcnode.pos:
                e.set_location(lineno=srcnode.pos.line)
            raise

    return annotate_errors


def set_pos(astnode, pos):
    if pos:
        astnode.lineno = pos.line
        astnode.col_offset = pos.char
    return astnode


def make_identifier(name):
    n = re.sub("[^a-zA-Z_0-9]", "_", str(name))
    if n[0] in "0123456789":
        n = "_" + n
    if n.startswith("__piglet"):
        raise ValueError('Indentifiers may not begin with "__piglet"')
    return n


def make_block_name(name):
    return f"__piglet_block_{make_identifier(name)}"


def compile_to_source(node, filename="<string>"):
    """
    Compile the given intermediate node to python source code.
    (Used for debugging/testing only, not called during normal operation)
    """
    return astunparse.unparse(compile_to_ast(node, filename))


def compile_to_ast(srcnode, filename="<string>"):
    """
    Compile the given intermediate node to an abstract syntax tree
    """
    c = Compiler(filename)
    return c.compile(srcnode)


def compile_to_codeob(ast_node, filename="<string>", saveas=None):
    """
    Compile the given intermediate or AST node to a python code object

    :param filename: filename of the template file
    :param saveas: Optional path to save the generated python code to.
                   This allows python to show the generated code in tracebacks
                   and allows stepping through template code in a debugger.
    """
    if not isinstance(ast_node, AST):
        ast_node = compile_to_ast(ast_node, filename)
    pysrc = astunparse.unparse(ast_node)
    if saveas:
        with io.open(saveas, "wb") as f:
            f.write(pysrc.encode("utf8"))
        return compile(pysrc, saveas, "exec")
    else:
        return compile(pysrc, filename, "exec")


def compile_to_module(codeob, filename, c=count(), bootstrap=None):
    """
    Compile the given python code object to a python module
    """
    if not isinstance(codeob, types.CodeType):
        codeob = compile_to_codeob(codeob, filename)
    fnhash = hashlib.sha256(filename.encode("UTF-8")).hexdigest()
    module_name = f"piglet_tmpl_{next(c)}_{fnhash}"
    module = types.ModuleType(module_name)
    if bootstrap is not None:
        module.__dict__.update(bootstrap)
    exec(codeob, module.__dict__)
    return module


class Compiler:
    """
    Implemented as a class, so that each compiler object gets its own
    ``uniquec`` instance, thus making generated identifiers stable
    """

    def __init__(self, filename):
        self.filename = filename
        self.uniquec = defaultdict(count)
        self.src_root = None
        self.module = Module(
            body=[
                ImportFrom(
                    module="piglet",
                    names=[alias(name="runtime", asname="__piglet_rt")],
                    level=0,
                ),
                ImportFrom(
                    module="piglet.exceptions",
                    names=[
                        alias(
                            name="TemplateNotFound",
                            asname="__piglet_TemplateNotFound",
                        )
                    ],
                    level=0,
                ),
            ]
        )

        # Store references to generated functions corresponding to nested
        # py:blocks to facilitate retro-fitting the necessary function
        # arguments up the call chain.
        self.block_chain = []

        self.module.body.extend(
            [
                Assign(
                    targets=[Name(id="Markup", ctx=Store())],
                    value=Attribute(
                        value=Name(id="__piglet_rt", ctx=Load()),
                        attr="Markup",
                        ctx=Load(),
                    ),
                ),
                Assign(
                    targets=[StoreName("__piglet_rtdata")],
                    value=LoadAttribute("__piglet_rt", "data"),
                ),
            ]
        )

    def unique_id(self, prefix="tmp"):
        """
        Generate a valid Python identifier, unique to this compiler instance.
        """
        return f"__piglet_{make_identifier(prefix)}{next(self.uniquec[prefix])}"

    def compile(self, im_root):
        """
        Compile a :class:`piglet.intermediate.RootNode` to an
        :class:`ast.Module` object
        """
        assert self.src_root is None, f"{self!r}.compile called more than once"

        try:
            self.src_root = im_root
            fn = self.create_function("__piglet_root__", self.module.body, im_root)
            add_arg_default(fn, make_arg("__piglet_bases"), List(elts=[], ctx=Load()))
            fn.args.kwarg = make_kwarg("__piglet_extra_blocks")
            module = self.module
            module = _hoist_variables_to_piglet_context(module)
            module = _ensure_all_functions_yield(module)
            module = _deduplicate_exception_annotations(module)
            module = add_locations(module)
        except PigletParseError as e:
            e.filename = self.filename
            raise
        return module

    @annotate_errors
    def _compile(self, srcnode, body):
        assert isinstance(srcnode, im.IntermediateNode)
        compile_fn = f"compile_{srcnode.__class__.__name__.lower()}"
        try:
            getattr(self, compile_fn)(srcnode, body)
        except SyntaxError as e:
            if " at template line" in e.args[0]:
                raise
            cls, _, tb = sys.exc_info()
            reraise(
                cls,
                SyntaxError(
                    f"{e.args[0]} at template line {srcnode.pos.line} {self.filename}"
                ),
                tb,
            )

    @annotate_errors
    def compile_containernode(self, srcnode, body):
        for item in srcnode.children:
            self._compile(item, body)

    @annotate_errors
    def compile_textnode(self, srcnode, body):
        expr = Expr(value=Yield(Str(srcnode.content)))
        set_pos(expr, srcnode.pos)
        body.append(expr)

    @annotate_errors
    def compile_blockreplacenode(self, srcnode, body):
        """
        Compile a BlockNode where it is used inside within an ExtendsNode
        (ie to replace the parent block)
        """
        return self.compile_blocknode(srcnode, body, "replace")

    @annotate_errors
    def compile_blocknode(self, srcnode, body, mode="define"):
        """
        Compile a BlockNode (<py:block>).

        :param mode: if 'define' this is a block definition; if 'replace'
                     this is a block being used inside an ExtendsNode to
                     replace the parent template's content.
        """
        assert mode in {"define", "replace"}

        block_funcname = block_name = make_block_name(srcnode.name)
        block_func = self.create_function(block_funcname, self.module.body)
        set_pos(block_func, srcnode.pos)
        # A template extending a parent template may override
        # a block without implementing one or more of the nested
        # subblocks from the parent template. The parent will still pass
        # references to the block functions when calling the extending
        # template's block, so we need to be able to accept these.
        add_arg_default(
            block_func, make_arg("__piglet_bases"), List(elts=[], ctx=Load())
        )
        block_func.args.kwarg = make_kwarg("__piglet_extra_blocks")
        block_func.body.extend(
            parse_and_strip(
                f"""
                super = __piglet_rt.get_super(
                    __piglet_bases,
                    __piglet_template,
                    '{block_funcname}'
                )
                """
            )
        )

        block_func_call = Call(
            func=LoadName(block_name),
            args=[],
            starargs=None,
            kwargs=None,
            keywords=[keyword(arg="__piglet_bases", value=LoadName("__piglet_bases"))],
        )
        add_kwarg(block_func_call, "__piglet_extra_blocks")

        # Push the current parent context onto the block chain. If nested
        # blocks are encountered, we need to be able to insert default
        # args for inner blocks all the way up the chain. For example::
        #
        #   <py:block name="page">
        #     <py:block name="head">
        #     </py:block>
        #   </py:block>
        #
        # Should generate the function signatures::
        #
        #   def __piglet_head0(...):
        #   def __piglet_page0(..., head=__piglet_head0):
        #   def __piglet_root__(..., page=__piglet_page0, head=__piglet_head0):
        #
        # When compiling the 'head' block, the compiler has to
        # go back and insert the 'head=__piglet_head0' arguments into
        # __piglet_page0 and __piglet_root__. That's what this data structure
        # is for.
        self.block_chain.append((self.get_func(body), block_func_call))

        # Insert this before existing functions block functions are
        # declared before the containing function. This is required because
        # a reference to the block function is placed in the containing
        # function's argument list
        for ix, n in enumerate(self.module.body):
            if isinstance(n, FunctionDef):
                self.module.body.insert(ix, block_func)
                break
        else:
            self.module.body.append(block_func)

        for item in srcnode.children:
            self._compile(item, block_func.body)

        # Recursively add this block's function as a keyword argument
        # throughout the caller chain
        for referent, referent_call in self.block_chain:
            add_arg_default(referent, make_arg(block_name), LoadName(block_funcname))
            if referent_call is not block_func_call:
                referent_call.keywords.append(
                    keyword(arg=block_name, value=LoadName(block_name))
                )

        self.block_chain.pop()

        if mode == "replace":
            return

        body.append(Expr(value=YieldFrom(value=block_func_call)))

    @annotate_errors
    def compile_includenode(self, srcnode, body):
        return self.compile_extendsnode(srcnode, body)

    @annotate_errors
    def compile_extendsnode(self, srcnode, body):
        if "$" in srcnode.href:
            value = _interpolated_str_to_ast_value(srcnode.href)
            body.append(Assign(targets=[StoreName("__piglet_tmp")], value=value))
            loadcode = "__piglet_rt.load(__piglet_template, __piglet_tmp)\n"
        else:
            loadcode = f'__piglet_rt.load(__piglet_template, "{srcnode.href}")\n'

        try_ = None
        if srcnode.ignore_missing is not False:
            try_ = Try(
                body=parse_and_strip(f"__piglet_parent = {loadcode}"),
                handlers=[
                    ExceptHandler(
                        type=LoadName("__piglet_TemplateNotFound"),
                        name=None,
                        body=Pass(),
                    )
                ],
                orelse=parse_and_strip(
                    "__piglet_bases = [__piglet_parent] + __piglet_bases\n"
                ),
                finalbody=[],
            )
            body.append(try_)
            container_body = try_.orelse
        else:
            container_body = body
            container_body.extend(
                parse_and_strip(
                    f"__piglet_parent = {loadcode}"
                    "__piglet_bases = [__piglet_parent] + __piglet_bases\n"
                )
            )

        for n in srcnode.children:
            if isinstance(n, im.BlockNode):
                self.compile_blockreplacenode(n, container_body)
            elif isinstance(n, im.DefNode):
                self._compile(n, container_body)

        block_ids = [make_block_name(n.name) for n in srcnode.find(im.BlockNode)]

        parent_template_call = Call(
            func=LoadAttribute("__piglet_parent", "__piglet_root__"),
            args=[],
            starargs=None,
            kwargs=None,
            keywords=(
                [keyword(arg="__piglet_bases", value=LoadName("__piglet_bases"))]
                + [keyword(arg=str(b), value=LoadName(str(b))) for b in block_ids]
            ),
        )
        add_kwarg(parent_template_call, "__piglet_extra_blocks")
        container_body.append(Expr(value=YieldFrom(value=parent_template_call)))

    @annotate_errors
    def compile_ifnode(self, srcnode, body):
        comparison = get_comparison(str(srcnode.test))
        if_ = If(test=comparison, body=[], orelse=[])
        body.append(self.annotate_runtime_errors(if_, srcnode))
        for item in srcnode.children:
            self._compile(item, if_.body)

        if srcnode.else_:
            for item in srcnode.else_.children:
                self._compile(item, if_.orelse)

        if if_.body == []:
            if_.body = [Pass()]

    @annotate_errors
    def compile_withnode(self, srcnode, body):
        # WithNodes can be constructed in compilexml with a list of
        # key-value pairs

        values = srcnode.get_pairs()
        values = [(self.unique_id("save"),) + item for item in values]
        marker = self.unique_id("marker")
        body.extend(parse_and_strip(f"{marker} = []"))

        for savevar, varname, value in values:
            body.append(
                self.annotate_runtime_errors(
                    parse_and_strip(
                        f"""
                        {savevar} = __piglet_ctx.get('{varname}', {marker})
                        {varname} = __piglet_ctx['{varname}'] = {value}
                        """
                    ),
                    srcnode,
                )
            )

        for item in srcnode.children:
            self._compile(item, body)

        for savevar, varname, value in values:
            body.extend(
                parse_and_strip(
                    f"""
                    if {savevar} is {marker}:
                        del __piglet_ctx['{varname}']
                        {varname} = __piglet_rt.Undefined('{varname}')
                    else:
                        {varname} = __piglet_ctx['{varname}'] = {savevar}
                    """
                )
            )

    @annotate_errors
    def compile_choosenode(self, srcnode, body):
        if srcnode.test is None or srcnode.test.strip() == "":
            srcnode.test = "True"

        choosevar = self.unique_id("choose")
        chooseflag = self.unique_id("chosen")

        body.append(
            self.annotate_runtime_errors(
                parse_and_strip(
                    f"""
                    {chooseflag} = False
                    {choosevar} = {srcnode.test}
                    """
                ),
                srcnode,
            )
        )

        for item in srcnode.children:
            if isinstance(item, im.WhenNode):
                comparison = get_comparison(
                    f"{chooseflag} is False and {choosevar} == ({item.test})"
                )
                if_ = If(test=comparison, body=[], orelse=[])
                if_.body.extend(parse_and_strip(f"{chooseflag} = True"))
                set_pos(if_, item.pos)
                body.append(self.annotate_runtime_errors(if_, srcnode))
                for sub in item.children:
                    self._compile(sub, if_.body)

            elif isinstance(item, im.OtherwiseNode):
                comparison = get_comparison(f"{chooseflag} is False")
                if_ = If(test=comparison, body=[], orelse=[])
                set_pos(if_, item.pos)
                body.append(if_)
                for sub in item.children:
                    self._compile(sub, if_.body)
                if if_.body == []:
                    if_.body = [Pass()]
            else:
                self._compile(item, body)

    @annotate_errors
    def compile_fornode(self, srcnode, body):
        for_ = parse_and_strip(f"for {srcnode.each}: pass")[0]
        for_.body = []
        set_pos(for_, srcnode.pos)
        body.append(self.annotate_runtime_errors(for_, srcnode))
        for item in srcnode.children:
            self._compile(item, for_.body)

    @annotate_errors
    def compile_interpolatenode(self, srcnode, body, mode="yield"):
        value = parse_and_strip(f"x = ({srcnode.value})")[0].value
        if srcnode.autoescape:
            escaped = Call(
                func=Name(id="__piglet_escape", ctx=Load()),
                args=[value],
                starargs=None,
                kwargs=None,
                keywords=[],
            )
        else:
            escaped = Call(
                func=Name(id="str", ctx=Load()),
                args=[value],
                starargs=None,
                kwargs=None,
                keywords=[],
            )

        body.append(self.annotate_runtime_errors(Expr(value=Yield(escaped)), srcnode))

    @annotate_errors
    def compile_importnode(self, srcnode, body):

        assign = Assign(
            targets=[Name(id=str(srcnode.alias), ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="__piglet_rt", ctx=Load()),
                    attr="load",
                    ctx=Load(),
                ),
                args=[
                    Name(id="__piglet_template", ctx=Load()),
                    Str(s=srcnode.href),
                ],
                starargs=None,
                kwargs=None,
                keywords=[],
            ),
        )
        assign = self.annotate_runtime_errors(assign, srcnode)

        func = self.get_func(body)
        if func.name == "__piglet_root__":
            self.module.body.insert(self.module.body.index(func), assign)
        else:
            func.body.append(assign)

    @annotate_errors
    def compile_inlinecodenode(self, srcnode, body):
        statements = parse_and_strip(srcnode.pysrc)
        if statements:
            set_pos(statements[0], srcnode.pos)
            body.append(self.annotate_runtime_errors(statements, srcnode))

    @annotate_errors
    def compile_translationnode(self, srcnode, body):
        translated = Call(
            func=LoadName("_"),
            args=[Str(srcnode.get_msgstr())],
            starargs=None,
            kwargs=None,
            keywords=[],
        )

        named_children = [
            (name, node) for name, node in srcnode.named_children() if name is not None
        ]

        if not named_children:
            # Simple case - no dynamic children for placeholder replacement
            body.append(Expr(value=Yield(translated)))
            return

        body.append(Assign(targets=[StoreName("__piglet_places")], value=Dict([], [])))

        for name, node in named_children:
            with self.collect_output(body) as ACC:
                self._compile(node, body)
                body.append(
                    Assign(
                        targets=[
                            Subscript(
                                value=LoadName("__piglet_places"),
                                slice=Index(value=Str(name)),
                                ctx=Store(),
                            )
                        ],
                        value=Call(
                            func=Attribute(value=Str(s=""), attr="join", ctx=Load()),
                            args=[LoadName(ACC)],
                            starargs=None,
                            kwargs=None,
                            keywords=[],
                        ),
                    )
                )

        for name, node in named_children:
            translated = Call(
                func=Attribute(value=translated, attr="replace", ctx=Load()),
                args=[
                    Str(f"${{{name}}}"),
                    Subscript(
                        value=LoadName("__piglet_places"),
                        slice=Index(value=Str(name)),
                        ctx=Load(),
                    ),
                ],
                starargs=None,
                kwargs=None,
                keywords=[],
            )
        set_pos(translated, srcnode.pos)
        body.append(Expr(value=Yield(translated)))

    @annotate_errors
    def compile_translationplaceholder(self, srcnode, body):
        for item in srcnode.children:
            self._compile(item, body)

    @annotate_errors
    def compile_call(self, srcnode, body):
        fn = srcnode.function
        if "(" not in fn:
            fn += "()"
        call = parse_and_strip(fn)[0].value
        leftovers = im.ContainerNode()
        for item in srcnode.children:
            if isinstance(item, im.CallKeyword):
                funcname = self.unique_id(item.name)
                self.create_function(funcname, body, item)
                call.keywords.append(keyword(arg=item.name, value=LoadName(funcname)))
            elif isinstance(item, im.TextNode) and is_whitespace(item.content):
                continue
            else:
                leftovers.children.append(item)

        if leftovers.children:
            funcname = self.unique_id()
            self.create_function(funcname, body, leftovers)
            call.args.append(make_arg(funcname))
        body.append(
            self.annotate_runtime_errors(
                Expr(
                    value=Yield(
                        Call(
                            func=LoadName("str"),
                            args=[call],
                            starargs=None,
                            kwargs=None,
                            keywords=[],
                        )
                    )
                ),
                srcnode,
            )
        )

    @annotate_errors
    def compile_defnode(self, srcnode, body):
        # Will be either "myfunc(arg1, arg2)" or just plain "myfunc"
        funcsig = srcnode.function

        if "(" not in funcsig:
            funcsig += "()"

        parsedsig = parse_and_strip(f"def {funcsig}: pass")[0]
        fn = self.create_function(parsedsig.name, self.module.body)
        fn.args = parsedsig.args
        set_pos(fn, srcnode.pos)
        # Create an empty block inheritance variables so that subsequent
        # <py:includes> have them to work with
        fn.body.extend(
            parse_and_strip("__piglet_bases = []\n__piglet_extra_blocks = {}\n")
        )
        for item in srcnode.children:
            self._compile(item, fn.body)

    def compile_comment(self, srcnode, body):
        return

    @annotate_errors
    def compile_filternode(self, srcnode, body):
        func = parse_and_strip(srcnode.function)[0].value

        with self.collect_output(body) as ACC:
            for node in srcnode.children:
                self._compile(node, body)

        joined = Call(
            func=Attribute(value=Str(s=""), attr="join", content=Load()),
            args=[LoadName(ACC)],
            starargs=None,
            kwargs=None,
            keywords=[],
        )
        body.append(
            Expr(
                value=Yield(
                    Call(
                        func=func,
                        args=[joined],
                        starargs=None,
                        kwargs=None,
                        keywords=[],
                    )
                )
            )
        )

    @annotate_errors
    def create_function(self, funcname, body=None, srcnode=None) -> FunctionDef:
        """
        Convenience function to create an ast.FunctionDef node and
        append it to the parent.

        :param funcname: name of the function
        :param body: list of nodes to append function to
        :param srcnode: source intermediate node
        :param append: append the created function node to the parent's body?
        """
        fn = FunctionDef(
            name=str(funcname),
            args=arguments(
                args=[],
                defaults=[],
                vararg=None,
                kwonlyargs=[],
                kwarg=None,
                kw_defaults=[],
            ),
            body=[],
            decorator_list=[
                Attribute(
                    value=Name(id="__piglet_rt", ctx=Load()),
                    attr="flatten",
                    ctx=Load(),
                )
            ],
            returns=None,
        )
        if body is not None:
            body.append(fn)
        self.add_builtins(fn)
        if srcnode:
            set_pos(fn, srcnode.pos)
            for item in srcnode.children:
                self._compile(item, fn.body)
        return fn

    def add_builtins(self, fn):
        fn.body.extend(
            [
                Assign(
                    targets=[Name(id="value_of", ctx=Store())],
                    value=Attribute(
                        value=Name(id="__piglet_ctx", ctx=Load()),
                        attr="get",
                        ctx=Load(),
                    ),
                ),
                Assign(
                    targets=[Name(id="defined", ctx=Store())],
                    value=Attribute(
                        value=Name(id="__piglet_ctx", ctx=Load()),
                        attr="__contains__",
                        ctx=Load(),
                    ),
                ),
                Assign(
                    targets=[Name(id="__piglet_escape", ctx=Store())],
                    value=Attribute(
                        value=Name(id="__piglet_rt", ctx=Load()),
                        attr="escape",
                        ctx=Load(),
                    ),
                ),
            ]
        )

    def get_ancestors(self, node):
        """
        Return the sequence of ancestor nodes for ``node``.
        :param astnode: the astnode to consider
        :yields: sequence of ancestor AST nodes, in the order
                ``[node, parent, grandparent, great-grandparent, ...]``
        """
        if isinstance(node, Sequence):
            dummy = Pass()
            node.append(dummy)
            try:
                return self.get_ancestors(dummy)
            finally:
                node.remove(dummy)
        for n, ancestors in astwalk(self.module):
            if n is node:
                return chain([node], reversed(ancestors))
        return []

    def get_func(self, node):
        """
        Return the containing AST FunctionDef object for ``node``
        """
        return next(n for n in self.get_ancestors(node) if isinstance(n, FunctionDef))

    @contextmanager
    def collect_output(self, body):
        """
        Context manager that collects any yield expressions added to ``body``
        and turns them into calls to ``__piglet_acc<n>.append``.

        The name of the accumulator object is returned by the function
        """
        acc = self.unique_id("acc")
        append = self.unique_id("append")
        pos = len(body)

        body.append(Assign(targets=[StoreName(acc)], value=List(elts=[], ctx=Load())))
        body.append(
            Assign(
                targets=[StoreName(append)],
                value=Attribute(value=LoadName(acc), attr="append", ctx=Load()),
            )
        )
        yield acc
        for n in body[pos:]:
            for node, ancestors in astwalk(n):
                if isinstance(node, Expr) and isinstance(node.value, Yield):
                    node.value = Call(
                        func=LoadName(append),
                        args=[node.value.value],
                        starargs=None,
                        kwargs=None,
                        keywords=[],
                    )

    def annotate_runtime_errors(self, body, imnode):
        from piglet.astutil import TryExcept

        if imnode.pos is None:
            raise ValueError("pos attribute not set on im node")
        handler = parse_and_strip(
            f"""
            getattr(__piglet_rtdata, "context", [{{}}])[-1]\
            .setdefault("__piglet_exc_locations", []).append(
                ({self.filename!r}, {imnode.pos.line!r})
            )
            raise
            """
        )
        if not isinstance(body, list):
            body = [body]

        te = TryExcept(
            body=body,
            handlers=[
                ExceptHandler(type=LoadName("Exception"), name=None, body=handler)
            ],
        )
        te.position = self.filename, imnode.pos.line
        return te


def _get_function_defs(astnode):
    return ((n, a) for n, a in astwalk(astnode) if isinstance(n, FunctionDef))


def _get_out_of_scope_names(fn):
    """
    Return the set of names that are not accessible within node ``fn``.

    This is good enough for the ast generated by piglet, but would not work
    more generally as it does not support global and non_local
    """
    in_scope = set()
    out_of_scope = set()

    for n, ancestors in astwalk(fn):
        # A function parameter or py2 variable assignment
        if isinstance(n, Name) and isinstance(n.ctx, (Param, Store)):
            in_scope.add((ancestors, n.id))

        # A py3 function argument
        elif arg is not None and isinstance(n, arg):
            in_scope.add((ancestors, n.arg))

        # A name defined through an import
        elif isinstance(n, alias):
            in_scope.add((ancestors, n.asname or n.name))

        # A reference to a (possibly non-local) variable
        elif isinstance(n, Name) and isinstance(n.ctx, Load):
            if not any(
                (ancestors[:ix], n.id) in in_scope for ix in range(len(ancestors) + 1)
            ):
                out_of_scope.add((n, ancestors))
    return out_of_scope


def _hoist_variables_to_piglet_context(astnode, exclude_functions=frozenset()):
    """
    Template functions extract all local variables from the
    :var:`piglet.runtime.data` thread local
    """

    # Names we never hoist.
    # "None" would raise a SyntaxError if we try assigning to it. The others
    # are used internally by piglet and need to be reserved.
    restricted_names = {
        "None",
        "True",
        "False",
        "value_of",
        "defined",
        "Markup",
        "iter",
        "AttributeError",
        "Exception",
        "print",
        "getattr",
    }

    # Mapping of function -> names used within function
    func_names = {}

    # Mapping of {function name: {<ancestor nodes>, ...}}
    func_ancestors = {}

    # All names discovered together with their ast location
    names = []

    for fn, ancestors in _get_function_defs(astnode):
        func_ancestors.setdefault(fn.name, set()).add(ancestors)
        func_names[fn] = set()

    is_reserved = lambda n: n.id in restricted_names
    is_piglet = lambda n: n.id.startswith("__piglet")
    is_function = lambda n, a: any(
        a[: len(fancestors)] == fancestors
        for fancestors in func_ancestors.get(n.id, set())
    )

    names = (
        (ancestors, node)
        for node, ancestors in _get_out_of_scope_names(astnode)
        if not (is_reserved(node) or is_piglet(node) or is_function(node, ancestors))
    )

    for ancestors, node in names:
        container_func = next(
            (a for a in reversed(ancestors) if isinstance(a, FunctionDef)),
            None,
        )
        if container_func in exclude_functions:
            continue
        if container_func is None:
            lineno = getattr(node, "lineno", "(unknown line number)")
            raise AssertionError(f"Unexpected variable found at {lineno}: {node.id}")
        func_names[container_func].add(node.id)

    for f, names in func_names.items():
        assignments = [
            Assign(
                targets=[StoreName("__piglet_ctx")],
                value=Subscript(
                    value=LoadAttribute("__piglet_rtdata.context"),
                    slice=Index(value=Num(n=-1)),
                    ctx=Load(),
                ),
            )
        ]

        for n in sorted(names):
            is_builtin = n in builtin_names
            if is_builtin:
                default = LoadAttribute(LoadAttribute("__piglet_rt", "builtins"), n)
            else:
                default = Call(
                    func=Attribute(
                        value=Name(id="__piglet_rt", ctx=Load()),
                        attr="Undefined",
                        ctx=Load(),
                    ),
                    args=[Str(s=n)],
                    starargs=None,
                    kwargs=None,
                    keywords=[],
                )

            value = Call(
                func=Attribute(
                    value=Name(id="__piglet_ctx", ctx=Load()),
                    attr="get",
                    ctx=Load(),
                ),
                args=[Str(s=n), default],
                starargs=None,
                kwargs=None,
                keywords=[],
            )

            a = Assign(targets=[Name(id=n, ctx=Store())], value=value)
            assignments.append(a)

        f.body[0:0] = assignments
    return astnode


def yield_value(self, value, srcnode=None):
    expr = Expr(value=Yield(value))
    if srcnode:
        set_pos(expr, srcnode.pos)
    return expr


def _ensure_all_functions_yield(module):
    """
    All generated functions should contain at least one yield statement.
    This walks the ast to insert a "yield ''" in functions that
    don't otherwise produce output (eg in the case of '<py:def
    function="a"></py:def>')
    """
    functions = {}
    yield_classes = (Yield, YieldFrom)
    for node, ancestors in astwalk(module):
        if isinstance(node, FunctionDef):
            functions.setdefault(node, False)
        elif isinstance(node, yield_classes):
            f = next(a for a in reversed(ancestors) if isinstance(a, FunctionDef))
            functions[f] = True

    for f in functions:
        if not functions[f]:
            f.body.append(Expr(Yield(Str(s=""))))

    return module


def _deduplicate_exception_annotations(node, lastpos=None, OMIT=[0], KEEP=[1]):
    from piglet import astutil

    def getpos(n):
        if isinstance(n, astutil._Try or astutil._TryExcept):
            return getattr(n, "position", None)
        return None

    def _deduplicate(node, lastpos=None):
        pos = getpos(node)
        if pos and lastpos == pos:
            action = OMIT
        else:
            action = KEEP

        lastpos = pos or lastpos
        children = getattr(node, "body", [])
        if children:
            children = [_deduplicate(n, lastpos) for n in node.body]
            node.body = []
            for action, n in children:
                if action is KEEP:
                    node.body.append(n)
                else:
                    node.body.extend(n.body)

        return action, node

    return _deduplicate(node)[1]


def _interpolated_str_to_ast_value(source):
    items = List(
        [
            (
                Str(item)
                if isinstance(item, str)
                else parse_and_strip(f"x = ({item.value})")[0].value
            )
            for item in interpolate.parse_interpolations(source)
        ],
        Load(),
    )
    return Call(
        func=Attribute(Str(""), "join", Load()),
        args=[items],
        starargs=None,
        kwargs=None,
        keywords=[],
    )

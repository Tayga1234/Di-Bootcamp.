# Copyright 2022 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import re
import json
import typing as t
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class UnrecognizedContext(ValueError):
    """
    The string or path could not be interpreted as a context data file or
    literal
    """


def load_context(
    str_or_path: t.Union[Path, str]
) -> t.Tuple[t.Mapping[str, t.Any], t.Optional[Path]]:

    s = str(str_or_path)
    if os.path.exists(s):
        for tell, loader in FILE_LOADERS:
            if tell(s):
                return loader(s)
    else:
        for tell, loader in LITERAL_LOADERS:
            if tell(s):
                return loader(s)
    raise UnrecognizedContext(str_or_path)


def load_expr(src):
    ns = {}
    code = compile("result_ = ({})".format(src), "<string>", "exec")
    exec(code, ns)
    return ns["result_"], None


def load_json_literal(s):
    return json.loads(s), None


def load_python_literal(s):
    src = s.split(":", 1)[1]
    return load_expr(src), None


def load_python_file(filename):
    with io.open(filename, "r", encoding=None) as f:
        source = f.read()
    ns = {"__file__": filename}
    code = compile(source, f.name, "exec")
    exec(code, ns)
    return ns, Path(filename)


def load_python_file_symbol(s):
    filename, symbol = s.rsplit(":", 1)
    data = load_python_file(filename)[symbol]
    if callable(data):
        return data()
    return data, Path(filename)


def load_md_file(s):
    import markdown

    path = Path(s)
    md = markdown.Markdown(extensions=["extra", "meta"])

    with path.open("r", encoding="utf-8") as f:
        html = md.convert(f.read())

    return {"html": html, "meta": md.Meta}, path


def load_rst_file(s):
    """
    See
    https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/core.py#L510
    for an example of how to set up a docutils publisher programatically
    """
    import docutils.core
    import docutils.readers.doctree
    import docutils.io
    from docutils import nodes

    meta = {}
    path = Path(s)
    with path.open("r", encoding="utf-8") as f:
        raw = f.read()

    doctree = docutils.core.publish_doctree(raw)

    def traverse(n, condition_path):

        if not condition_path:
            yield n
            return

        for child in n.traverse(condition_path[0]):
            yield from traverse(child, condition_path[1:])

    def first(n, condition_path, default=None):

        try:
            return next(iter(traverse(n, condition_path)))
        except StopIteration:
            return default

    for node in doctree.traverse(nodes.field):
        try:
            name = first(node, [nodes.field_name, nodes.Text]).astext()
            value = first(node, [nodes.field_body, nodes.Text]).astext().strip()
            meta[name] = value
        except AttributeError:
            pass
    date = first(doctree, [nodes.date, nodes.Text])
    if date is not None:
        meta["date"] = date.astext()

    docinfo = first(doctree, [nodes.docinfo])
    if docinfo is not None:
        doctree.remove(docinfo)

    reader = docutils.readers.doctree.Reader(parser_name="null")
    pub = docutils.core.Publisher(
        reader,
        None,
        writer=None,
        source=docutils.io.DocTreeInput(doctree),
        destination_class=docutils.io.StringOutput,
        settings=None,
    )
    pub.set_writer("html")
    pub.process_programmatic_settings(None, None, None)
    pub.set_destination(None, None)
    pub.publish()
    parts = pub.writer.parts

    return {
        "title": parts["title"],
        "meta": meta,
        "html": parts["html_body"],
        "html_without_title": parts["body"],
        "parts": parts,
    }, path


def load_json_file(s):
    path = Path(s)
    with path.open("r", encoding="UTF-8") as f:
        content = f.read()
        return json.loads(content), path


def load_python_module(s):
    from importlib import import_module

    module = import_module(s)
    return vars(module), Path(module.__file__)


def load_python_module_symbol(s):
    mod, sym = s.rsplit(":", 1)
    modvars, path = load_python_module(mod)
    return modvars[sym], path


def expand_source_path(
    item: t.Union[Path, str],
    base: t.Optional[Path] = None,
) -> t.Iterable[t.Union[t.Tuple[Path, t.Optional[Path]], t.Tuple[str, None]]]:
    path = Path(item)
    if not path.exists():
        logger.warning(f"Source {path!r} not found")
        return
    if path.is_dir():
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                yield from expand_source_path(Path(dirpath) / f, base or path)
    else:
        yield path, base


def _match(s):
    return re.compile(s).match


LITERAL_LOADERS = [
    (_match(r"py(thon)?:"), load_python_literal),
    (_match(r"\s*\{"), load_json_literal),
    (_match(r".*\.py:"), load_python_file_symbol),
]
FILE_LOADERS = [
    (_match(r".*\.py$"), load_python_file),
    (_match(r".*\.rst$"), load_rst_file),
    (_match(r".*\.md$"), load_md_file),
    (_match(r".*\.js(on)?$"), load_json_file),
    (
        _match(r"([_A-Za-z][_A-Za-z0-9]*)(\.[_A-Za-z][_A-Za-z0-9]*)*$"),
        load_python_module,
    ),
    (
        _match(
            r"([_A-Za-z][_A-Za-z0-9]*)"
            r"(\.[_A-Za-z][_A-Za-z0-9]*)*"
            r":[_A-Za-z][_A-Za-z0-9]*$"
        ),
        load_python_module_symbol,
    ),
]

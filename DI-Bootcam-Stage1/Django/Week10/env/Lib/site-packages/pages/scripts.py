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

import logging
import typing as t
import os
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from functools import partial
from textwrap import dedent
from pages.templating import render
from pages.templating import load_plugins
from pages.templating import is_template_path
from pages.dataloaders import load_context
from pages.dataloaders import expand_source_path

logger = logging.getLogger(__name__)


def main(args=None):
    """
    Merge source files into an HTML template, outputting one
    HTML file per data source specified.
    Input files may be text formatted with reStructuredText, markdown, or
    data provided as JSON files or as Python source modules.
    """
    if args is None:
        return main(merge_parser.parse_args())
    if args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose >= 1:
        logging.basicConfig(level=logging.INFO)
    template = Path(args.template)

    if args.replace_path:
        search, replace = args.replace_path
        replace_path = partial(re.compile(search).sub, replace)
    else:
        replace_path = lambda x: x

    context = {}
    context_paths = []
    for d in args.context:
        data, path = load_context(d)
        context.update(data)
        if path is not None:
            context_paths.append(path)

    # Reverse sources so that later sources take priority. This facilitates the
    # pattern
    #
    #     pages -t template.html ... src/ src/data.json:another-template.html
    #
    sources = reversed(args.sources)
    if not args.sources or args.sources == ["-"]:
        sources = (line.rstrip("\r\n") for line in sys.stdin)
    sources_with_templates = map(_split_templates, sources)

    cwd = Path(".")
    seen = set()
    expanded_sources = (
        (input_path, relto, s_template)
        for s_path, s_template in sources_with_templates
        for input_path, relto in expand_source_path(s_path)
    )
    for input_path, relto, source_template in expanded_sources:
        if input_path in seen:
            continue
        seen.add(input_path)
        if is_template_path(input_path):
            _template = input_path
            data = {}
        else:
            data, input_path = load_context(input_path)
            _template = source_template if source_template else template

        if relto is None:
            relto = cwd
            if args.strip > 0:
                parent_index = -min(len(input_path.parents) - 1, args.strip) - 1
                relto = relto.joinpath(list(input_path.parents)[parent_index])
        path = Path(replace_path(str(input_path)))
        parents = list(path.parents)
        relpaths = [path]
        for n in range(-2, -5, -1):
            try:
                relpaths.append(path.relative_to(parents[n]))
            except IndexError:
                relpaths.append(relpaths[-1])
        if args.output_filename:
            output_filename = Path(
                args.output_filename.format(
                    path,
                    path0=relpaths[0],
                    path1=relpaths[1],
                    path2=relpaths[2],
                    path3=relpaths[3],
                    input=path,
                    path=path,
                )
            )
        else:
            output_filename = Path(f"{path.parent / path.stem}.html")
        if args.output:
            output = Path(args.output) / output_filename.relative_to(relto)
        else:
            output = output_filename
        logger.info(f"Rendering {input_path} to {output}")

        if args.update:
            deps = [input_path, _template] + context_paths
            if _is_up_to_date(output, deps):
                logger.info(f"Skipping {output}, already up to date")
                continue

        try:
            output.parent.mkdir(parents=True)
        except OSError:
            pass

        with output.open("wb") as f:
            render(
                _template,
                f,
                args.render_with,
                args.template_dir,
                {
                    "template_path": template,
                    "output_path": output,
                    "merge_path": path,
                },
                data,
                context,
            )


def _is_up_to_date(path, deps):
    if not path.exists():
        return False
    path_mtime = path.stat().st_mtime
    return all(not d.exists() or d.stat().st_mtime < path_mtime for d in deps)


def _split_templates(s: str) -> t.Tuple[str, t.Optional[str]]:
    if ":" in s:
        s_, template = s.rsplit(":", 1)
        if os.path.exists(template) and os.path.exists(s_):
            return s_, template
    return s, None


merge_parser = ArgumentParser(description=main.__doc__)
plugin_names = [p.name for p in load_plugins()] + ["auto"]
data_formats_help = dedent(
    """
    Data may be specified in the following formats:
    a json literal (eg {flag} \'{{"foo": "bar"}}\'); '
    a python function, which must return a dict
    (eg {flag} foo.py:get_data);
    a python module (eg {flag} foo.py);
    a restructured text file (eg --data foo.rst);
    a python expression,
    (eg {flag} 'python:{{\"foo\": \"bar\"}}').
    """
).strip()

args: t.Dict[str, t.Dict[str, t.Any]] = {
    "template": dict(help="Layout template into which data sources will be merged"),
    "template_dir": dict(help="Template search directory", nargs="*"),
    "render_with": dict(
        help=f"Templating system. Choose from {','.join(plugin_names)}",
        metavar="",
        choices=plugin_names,
        default="auto",
    ),
    "replace_path": dict(
        help=(
            "Regular expression search pattern "
            "and replacement to transform the path"
            "eg --replace-path '\\.rst$' '.html'"
        ),
        nargs=2,
    ),
    "output": dict(help="Output directory"),
    "output_filename": dict(
        help=(
            """
            Output filespec, eg 'build/{input.stem}.html'
            The variable '{input}' contains the path
            to the input file;
            '{path}' contains the same path
            transformed via --replace-path (if specified).
            '{path1}' expands to {path} with the first path segment stripped,
            '{path2}' with the first 2 path segments stripped and '{path3}' with
            the first 3 stripped.
            These are all pathlib.Path objects, so
            attributes such as 'path.parent' and 'path.stem'
            are available.
            """
        )
    ),
    "strip": dict(
        help="""
            Number of leading directory levels to strip off the input path when
            constructing the output path.
            ``--strip 1`` will write 'src/foo/index.html' into '<dest>/foo/index.html';
            ``--strip 2`` will result in '<dest>/index.html' and so on.
        """,
        type=int,
        default=0,
    ),
    "context": dict(
        help=(
            "Template context data source. "
            + data_formats_help.format(flag="--context")
        ),
        default=[],
        action="append",
    ),
    "sources": dict(
        help=dedent(
            """
            Data source files. An output file will be created
            for each input source found.

            If no data source files are given the list of files will be read
            from stdin.

            Any of the following data file formats may be used:

            a JSON literal (eg --data '{"x": 1}');
            a restructured text file (eg --data foo.rst);
            a markdown file (eg --data foo.md);
            a python module (eg --data foo.py or --data mypackage.mymodule:somevar);
            a python literal (eg --data "py:{'foo': 'bar'}"

            Templates may be specified per data source with `--data '<source-path>:<template-path>'`.
            """
        ).strip(),
        nargs="*",
    ),
    "update": dict(
        help=dedent(
            """
            Only update files that are out of date. This is determined by
            looking comparing the mtime of the destination with the source
            file, the layout template and any context data files specified.
            """
        ),
        action="store_true",
    ),
}

merge_parser.add_argument("-v", "--verbose", action="count", default=0)
merge_parser.add_argument("-t", "--template", **args["template"], required=True)
merge_parser.add_argument("-i", "--template-dir", **args["template_dir"])
merge_parser.add_argument("-r", "--render-with", **args["render_with"])
merge_parser.add_argument("--replace-path", **args["replace_path"])
merge_parser.add_argument("-o", "--output", **args["output"])
merge_parser.add_argument("-p", "--strip", **args["strip"])
merge_parser.add_argument("--output-filename", **args["output_filename"])
merge_parser.add_argument("--context", "-c", **args["context"])
merge_parser.add_argument("--update", "-u", **args["update"])
merge_parser.add_argument("sources", **args["sources"])

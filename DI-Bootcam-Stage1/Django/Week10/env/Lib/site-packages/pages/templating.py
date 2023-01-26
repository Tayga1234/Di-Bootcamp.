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

from pathlib import Path
from importlib_metadata import entry_points

_plugins = {}


def load_plugins():
    return entry_points(group="pages.template_plugins")


def get_plugin(name):
    if name in _plugins:
        return _plugins[name]
    entrypoint = load_plugins()[name]
    _plugins[name] = entrypoint.load()
    return _plugins[name]


def render(template, out, system, searchdirs, *context):
    searchdirs = template_dir_paths(searchdirs)
    path = next(find_template(template, searchdirs), None)
    if path is None:
        raise Exception("Path {} not found in {}".format(template, searchdirs))

    with path.open("r", encoding="UTF-8") as f:
        chunk = f.read(8192)
    if system == "auto":
        system = sniff_template(chunk)

    renderer = get_plugin(system)(template_dirs=searchdirs)
    out.write(renderer(template, *context).encode("UTF-8"))


def sniff_template(template):

    if "genshi.edgewall.org" in template:
        return "genshi"

    if "py:" in template:
        return "piglet"

    if "tal:" in template:
        return "chameleon"

    if ("{" + "{") in template or "{%" in template:
        return "jinja2"

    if "${" in template:
        return "piglet"

    return "piglet"


def template_dir_paths(dirs):
    if dirs:
        return [Path(t).resolve() for t in dirs]
    else:
        return [Path.cwd()]


def find_template(path, template_dirs, relative=False):
    for d in template_dirs:
        try:
            candidate = (d / path).resolve()
        except FileNotFoundError:
            continue
        if candidate.is_file():
            if relative:
                yield candidate.relative_to(d)
            else:
                yield candidate


def is_template_path(
    path: Path,
    template_suffixes=frozenset([".html", ".htm", ".tmpl", ".jinja2", ".htm"]),
):
    return any(s in template_suffixes for s in path.suffixes)


class TemplateRenderer:
    def __init__(self, template_dirs=None):
        self.template_dirs = template_dir_paths(template_dirs)
        self.loader = self.make_loader()

    def __call__(self, src, *context_stack):
        if isinstance(src, str):
            context = {"path": src}
            for c in context_stack:
                context.update(c)
            return self.render(src, context)

        if isinstance(src, Path):
            path = next(find_template(src, self.template_dirs, relative=True), None)
            if path is None:
                raise FileNotFoundError(
                    "Path {} not found in {}".format(src, self.template_dirs)
                )
            return self(str(path), *context_stack)

        raise TypeError("Can't render object of type {}".format(type(src)))

    def make_loader(self):
        raise NotImplementedError()

    def render(self, path, context):
        raise NotImplementedError()

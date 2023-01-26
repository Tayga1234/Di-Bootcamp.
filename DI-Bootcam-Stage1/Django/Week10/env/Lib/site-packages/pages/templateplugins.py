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

from pages.templating import TemplateRenderer


class GenshiRenderer(TemplateRenderer):
    def make_loader(self):
        from genshi.template import TemplateLoader

        self.loader = TemplateLoader([str(t) for t in self.template_dirs])

    def render(self, path, context):
        tmpl = self.loader.load(path)
        return tmpl.generate(**context).render("html")


class ChameleonRenderer(TemplateRenderer):
    def make_loader(self):
        from chameleon import PageTemplateLoader

        return PageTemplateLoader(
            [str(t) for t in self.template_dirs], auto_reload=True
        )

    def render(self, path, context):
        tmpl = self.loader.load(path)
        return tmpl.render(**context)


class KajikiRenderer(TemplateRenderer):
    def make_loader(self):
        from kajiki.loader import FileLoader

        return FileLoader([str(t) for t in self.template_dirs], reload=True)

    def render(self, path, context):
        return self.loader.import_(path)(context).render()


class PigletRenderer(TemplateRenderer):
    def make_loader(self):
        from piglet import TemplateLoader

        return TemplateLoader([str(t) for t in self.template_dirs])

    def render(self, path, context):
        return self.loader.load(path).render(context)
        import statprof

        with statprof.profile():
            return self.loader.load(path).render(context)


class KajikiXMLRenderer(KajikiRenderer):
    def make_loader(self):
        from kajiki.loader import FileLoader

        return FileLoader(
            [str(t) for t in self.template_dirs], reload=True, force_mode="xml"
        )


class KajikiTextRenderer(KajikiRenderer):
    def make_loader(self):
        from kajiki.loader import FileLoader

        return FileLoader(
            [str(t) for t in self.template_dirs],
            reload=True,
            force_mode="text",
        )


class Jinja2Renderer(TemplateRenderer):
    def make_loader(self):
        from jinja2 import Environment
        from jinja2 import FileSystemLoader

        return Environment(
            loader=FileSystemLoader([str(t) for t in self.template_dirs])
        )

    def render(self, path, context):
        return self.loader.get_template(path).render(**context)

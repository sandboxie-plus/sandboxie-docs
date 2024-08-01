import re

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


def _replacer(content):
    return re.sub(r'(\[.*]\(\s*)docs/(.*\))', r'\1\2', content)


class RootReadmeConfig(Config):
    readme = Type(str, default='readme.md')


class RootReadme(BasePlugin[RootReadmeConfig]):
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files):
        if self.config.readme and page.is_index:
            with open(self.config.readme) as f:
                readme = f.read()
            return _replacer(readme)

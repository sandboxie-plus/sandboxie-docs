import os
import shutil
from pathlib import PurePath

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin


class DirUrlMixConfig(Config):
    detect = Type(str, default='index.html')


class DirUrlMix(BasePlugin[DirUrlMixConfig]):

    def on_post_build(self, config: MkDocsConfig):
        skip = True
        site_dir = PurePath(config.site_dir)
        for root, dirs, files in os.walk(config.site_dir):
            root_path = PurePath(root)
            if skip and root_path == site_dir:
                skip = False
                continue
            for file in files:
                if file != self.config.detect:
                    continue
                shutil.copy(root_path / file, root_path.parent / f'{root_path.name}.html')

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. Suto-Commune
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : server.py

@Author     : Natsumi

@Date       : 2023/7/25 0:00
"""

import fnmatch
import importlib
import logging
import os
from functools import partial
from pathlib import Path

from sanic import Sanic
from sanic.worker.loader import AppLoader

from src.toml_config import config


class Server:
    """
    The main class of AntaresViewer server.
    """

    def __init__(self):
        """
        Placeholder.
        """
        pass

    @staticmethod
    def app_init(app_name: str) -> Sanic:
        """
        Init app and register blueprints.
        :param app_name:
        :return:
        """
        # Init app.
        app = Sanic(app_name)

        def get_py_files(path: Path):
            """
            Get all python files in the given path.
            """
            for root, dirs, files in os.walk(path):
                # Get all files that end with .py
                yield from (Path(root) / file for file in fnmatch.filter(files, '*.py'))

        for i, v in enumerate(get_py_files(Path("src/event"))):
            # Standardize the path.
            m = v.as_posix().replace('\\', "/").replace('./', "").replace('/', ".").replace(".py", "")

            # Load module.
            logging.info(f"Load {m}.")
            module = importlib.import_module(m)

            # Register blueprint.
            app.blueprint(module.bp)
        return app

    def both_init(self):
        """
        Init Sanic app and AppLoader.
        :return:
        """
        # 设置应用名称
        # Set app name.
        app_name = "AntaresViewer"

        # 创建AppLoader并传入应用创建函数
        # Create `AppLoader` and pass the app create function.
        loader = AppLoader(factory=partial(self.app_init, app_name))

        # 加载应用.
        # Load `Sanic` application.
        app = loader.load()
        return app, loader

    def launch(self):
        """
        Launcher AntaresViewer server.
        :return:
        """
        # 配置应用参数并启动.
        # Init and start.
        app, loader = self.both_init()
        app.prepare(host=config["server"]["host"],
                    port=config["server"]["port"],
                    workers=config["server"]["workers"],
                    fast=config["server"]["fast"],
                    access_log=config["server"]["access_log"],
                    dev=config["server"]["dev"] if not config["server"]["production"] else False,
                    debug=config["server"]["debug"] if not config["server"]["production"] else False)
        Sanic.serve(primary=app, app_loader=loader)

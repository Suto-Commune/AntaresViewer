<<<<<<< HEAD
import logging
import os
import fnmatch
import importlib
from src.toml_config import config
=======
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
from functools import partial
>>>>>>> 1360fd9e24ed5443cb35a440493e7321ff45947c

from functools import partial
from sanic import Sanic
from sanic.worker.loader import AppLoader


class Server:
    @staticmethod
    def app_init(app_name: str) -> Sanic:
        app = Sanic(app_name)
        py_files = []
        for root, dirs, files in os.walk(r"./src/event"):
            for file in fnmatch.filter(files, '*.py'):
                py_files.append(os.path.join(root, file))

        for i in range(len(py_files)):
            py_files[i] = py_files[i].replace('\\', "/").replace('./', "").replace('/', ".").replace(".py", "")
            m = py_files[i]
            logging.info(f"Load {m}.")
            module = importlib.import_module(py_files[i])
            app.blueprint(module.bp)
        return app

    def both_init(self):
        # 设置应用名称
        app_name = "AntaresViewer"
        # app = Sanic(app_name)
        # 创建AppLoader并传入应用创建函数

        loader = AppLoader(factory=partial(self.app_init, app_name))
        # 加载应用
        app = loader.load()
        return app, loader

    def launcher(self):
        # 配置应用参数并启动
        app, loader = self.both_init()
        app.prepare(host=config["server"]["host"],
                    port=config["server"]["port"],
                    workers=config["server"]["workers"],
                    fast=config["server"]["fast"],
                    access_log=config["server"]["access_log"],
                    dev=config["server"]["dev"] if not config["server"]["production"] else False,
                    debug=config["server"]["debug"] if not config["server"]["production"] else False)
        Sanic.serve(primary=app, app_loader=loader)

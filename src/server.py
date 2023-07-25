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

from sanic import Request, Sanic, json
from sanic.worker.loader import AppLoader


class Server:
    """
    The main class of AntaresViewer server.
    """

    @staticmethod
    def define_app(app_name: str) -> Sanic:
        """
        Init app and register handler.
        :param app_name:
        :return:
        """
        app = Sanic(app_name)

        @app.get("/")
        async def handler(request: Request):
            return json({"app_name": request.app.name})

        return app

    def define_app_and_loader(self) -> (Sanic, AppLoader):
        """
        Init Sanic app and AppLoader.
        :return:
        """
        # 设置应用名称
        # Set app name.
        app_name = "AntaresViewer"
        # app = Sanic(app_name)

        # 创建AppLoader并传入应用创建函数
        # Create `AppLoader` and pass the app create function.
        loader = AppLoader(factory=partial(self.define_app, app_name))
        loader = AppLoader(factory=Sanic(app_name))

        # 加载应用.
        # Load `Sanic` application.
        app = loader.load()
        return app, loader

    def launcher(self):
        """
        Launcher AntaresViewer server.
        :return:
        """
        # 配置应用参数并启动.
        # Init and start.
        app, loader = self.define_app_and_loader()
        app.prepare(port=9999, dev=True)
        Sanic.serve(primary=app, app_loader=loader)

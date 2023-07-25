import sys
from functools import partial

from sanic import Request, Sanic, json
from sanic.worker.loader import AppLoader


class Server:

    @staticmethod
    def define_app(app_name: str) -> Sanic:
        app = Sanic(app_name)

        @app.get("/")
        async def handler(request: Request):
            return json({"app_name": request.app.name})

        return app

    def define_app_and_loader(self):
        # 设置应用名称
        app_name = "AntaresViewer"
        # app = Sanic(app_name)
        # 创建AppLoader并传入应用创建函数

        loader = AppLoader(factory=partial(self.define_app, app_name))
        loader = AppLoader(factory=Sanic(app_name))
        # 加载应用
        app = loader.load()
        return app, loader

    def launcher(self):
        # 配置应用参数并启动
        app, loader = self.define_app_and_loader()
        app.prepare(port=9999, dev=True)
        Sanic.serve(primary=app, app_loader=loader)

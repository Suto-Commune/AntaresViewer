import logging
import os
import fnmatch
import importlib
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
            py_files[i] = py_files[i].replace('\\', "/").replace('./', "").replace('/', ".").replace(".py","")
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
        app.prepare(port=9999, dev=True)
        Sanic.serve(primary=app, app_loader=loader)

from pathlib import Path

import fastapi
import os
import importlib


class App:
    def __init__(self):
        self.app = fastapi.FastAPI()
        self.register_route()

    @staticmethod
    def find_python_files(directory):
        for root, dirs, files in os.walk(directory):
            root_ = Path(root)
            yield from map(lambda x: root_ / x, filter(lambda x: x.endswith(".py"), files))

    def register_route(self):
        py_files = filter(lambda x: "__init__.py" not in x.as_posix(), self.find_python_files("./src/server/event"))

        for i in py_files:
            i = i.as_posix().replace("\\", "/").replace("./", "").replace("/", ".").replace(".py", "")
            self.app.include_router(importlib.import_module(i).router)


App = App()
app = App.app

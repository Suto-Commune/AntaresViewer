import fastapi
import os
import importlib


class App:
    def __init__(self):
        self.app = fastapi.FastAPI()
        self.register_route()

    @staticmethod
    def find_python_files(directory):
        python_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files

    def register_route(self):
        py_files = self.find_python_files("./src/server/event")
        py_files = [file for file in py_files if "__init__.py" not in file]
        modules = []
        for i in range(len(py_files)):
            py_files[i] = py_files[i].replace("\\", "/").replace("./", "").replace("/", ".").replace(".py", "")
            modules.append(importlib.import_module(py_files[i]))
        for i in modules:
            self.app.include_router(i.router)


App = App()
app = App.app

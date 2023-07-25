from sanic import Sanic


class Server:
    def __init__(self):
        self.app = Sanic("AntaresViewer")

    def launcher(self):
        self.app.run("0.0.0.0", 8000, auto_reload=True,workers=1)

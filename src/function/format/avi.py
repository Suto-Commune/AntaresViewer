import inspect


class Name:
    def __init__(self):
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        self.caller_name = caller_module.__name__
        self.default_url='/'+str(self.caller_name).replace("src.server.event.", "").replace(".", "/")

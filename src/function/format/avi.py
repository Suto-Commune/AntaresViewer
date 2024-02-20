import inspect
import re


# 存储关键信息的类


class Name:
    def __init__(self):
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        self.caller_name = caller_module.__name__
        self.default_url = '/' + str(self.caller_name).replace("src.server.event.", "").replace(".", "/")


def is_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email) is not None

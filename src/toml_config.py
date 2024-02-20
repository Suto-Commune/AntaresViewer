import tomllib
from box import Box


def read_config():
    path = "./config.toml"
    with open(path, "rb") as f:
        toml_config = tomllib.load(f)
    f.close()
    return Box(toml_config) #对象化


config = read_config()

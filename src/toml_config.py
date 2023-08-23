import tomllib


def read_config():
    path = "./config.toml"
    with open(path, "rb") as f:
        toml_config = tomllib.load(f)
    return toml_config


config = read_config()

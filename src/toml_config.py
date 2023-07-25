import tomllib


def read_config():
    path = "./config.toml"
    with open(path, "r", encoding="UTF-8") as f:
        toml_config = tomllib.loads(f.read())
        f.close()
    return toml_config


config = read_config()

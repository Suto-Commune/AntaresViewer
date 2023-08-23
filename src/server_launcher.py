import uvicorn
from src.toml_config import config


class Server:
    def __init__(self):
        self.server_config = config["server"]

    def launch(self):
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(levelname)s][uvicorn] %(message)s",
                    "datafmt": "%b/%d/%Y-%H:%M:%S"
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            },
        }
        uvicorn.run("src.server.api:app", host=self.server_config["host"], port=self.server_config["port"],
                    workers=self.server_config["workers"] if self.server_config["workers"] != 0 else None,
                    reload=self.server_config["reload"], access_log=self.server_config["access_log"]
                    , log_config=log_config)

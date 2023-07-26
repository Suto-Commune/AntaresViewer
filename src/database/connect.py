from src.toml_config import config
import pymongo


class Database:
    def __init__(self, database_name):
        self.client = pymongo.MongoClient(config["database"]["url"])
        self.db = self.client[database_name]

import json
import os
from pathlib import Path


class DataBlock:
    def __init__(self, path, name):
        ...
        self.path = Path("src/data/" + path)
        self.name = name
        self.fullpath = self.path / (self.name + ".json")

    def create(self):
        if not os.path.exists(self.fullpath):
            with open(self.fullpath, "w", encoding="UTF-8") as f:
                f.close()

    def diiiict(self):

        with self.fullpath.open(encoding='utf-8') as f:
            if len(f.read().strip()) == 0:
                print(1)
                return None
            else:
                f.seek(0)
                back = json.load(f)
        return back

    def update(self, something_to_write: dict):
        with open(self.fullpath, "w", encoding="UTF-8") as f:
            json.dump(something_to_write, f)
            f.close()

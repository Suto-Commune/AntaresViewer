import fastapi
import src.function.format.avi as AVI
import hashlib
from typing import Union
import src.data.datablock as datablock
import src.function.interesting.random_string as random_string

Name = AVI.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
async def register(username: str, password: str, sid: Union[str, None] = None):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    sha256_hex = sha256_hash.hexdigest()
    user = {
        "username": username,
        "password": sha256_hex
    }
    DB = datablock.DataBlock("", "users")
    DB.create()
    info = DB.diiiict()
    if sid is None:
        sid = random_string.random_string()

    if info is None:
        info = {"users": []}
        user["id"] = 0
    else:
        info=info
        user["id"] = len(info["users"])
    user["sid"] = sid
    info["users"].append(user)
    DB.update(info)
    print(user)
    return {"Hello,AntaresViewer"}

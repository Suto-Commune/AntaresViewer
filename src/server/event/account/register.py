import os
import uuid
from typing import Union

import fastapi

import src.data.datablock as datablock
import src.function.format.avi as AVI
import src.function.interesting.random_string as random_string
from src.utils.crypto import password_hash

Name = AVI.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
async def register(username: str, password: str):
    # Get password hash
    _hash = password_hash(password=password, n=16384, r=8, p=1, maxmem=0, dklen=64)
    user = {
        "username": username,
        "password": _hash
    }

    # Init db
    DB = datablock.DataBlock("", "users")
    DB.create()
    info = DB.diiiict()



    # Check if info is empty
    if info:
        user["id"] = len(info["users"])
    else:
        info = {"users": []}
        user["id"] = 0

    user["uid"] = uuid.uuid4().hex
    info["users"].append(user)

    # Write to db
    DB.update(info)

    return {"Hello,AntaresViewer"}

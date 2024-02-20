import uuid

import fastapi

import src.function.format.avi as AVInfo
from src.function.database.db import DB
from src.toml_config import config
from src.utils.crypto import password_hash
import logging

logger = logging.getLogger(__name__)
Name = AVInfo.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
@router.post(default_url)
async def register(email: str, username: str, password: str):
    # Get password hash
    _hash = password_hash(password=password, n=16384, r=8, p=1, maxmem=0, dklen=64)
    if not AVInfo.is_valid_email(email):
        return {"code": "403", "message": "Email format error."}  # 格式错误
    user = {
        "email": email,
        "username": username,
        "password": _hash
    }

    # Init db
    print(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    db = DB(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    uid = uuid.uuid4().hex
    user["uid"] = uid
    result = await db.insert("users", user)
    print(result)
    return {"code": "200", "uid": uid}

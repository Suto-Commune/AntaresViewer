import logging
import uuid

import fastapi
from passlib.context import CryptContext

import src.function.format.avi as AVInfo
from src.data.containers.user import User
from src.function.database.db import DB
from src.toml_config import config

logger = logging.getLogger(__name__)
Name = AVInfo.Name()
default_url = Name.default_url
router = fastapi.APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get(default_url)
@router.post(default_url)
async def register(email: str, username: str, password: str):
    # Get password hash
    _hash = pwd_context.hash(password)

    if not AVInfo.is_valid_email(email):
        return {"code": "403", "message": "Email format error."}  # 格式错误


    # Init db
    print(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    db = DB(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    uid = uuid.uuid4().hex
    user = User(
        email=email,
        username=username,
        password=_hash,
        uid=uid
    )
    result = await db.insert("users", user.dump())
    print(result)
    return {"code": "200", "uid": uid}

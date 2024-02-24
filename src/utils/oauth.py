#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. Suto-Commune
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : oauth.py

@Author     : hsn

@Date       : 2/20/24 9:05 PM
"""
from pathlib import Path

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.data.containers.user import UserWithSession
from src.function.database.db import DB
from src.toml_config import config
from src.utils.crypto import JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    with Path("server.key").open("r", encoding="utf-8") as f:
        key = f.read()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWT(key).decode(token)
        username: str = payload.get("uid")
        if username is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception
    db = DB(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)
    rst = await db.find("users", {"uid": username})
    user_dict: dict = rst[0]
    if payload.get("session") not in user_dict.get("active_sessions", {}):
        raise credentials_exception
    if not user_dict:
        raise credentials_exception

    user_dict.update(payload)
    user_dict.pop("_id")
    user_dict.pop("exp")

    user = UserWithSession(**user_dict)

    async def callback(data: dict):
        for k, v in data.items():
            await db.update("users", {"uid": username}, k, v)

    user.set_save_callback(callback)
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

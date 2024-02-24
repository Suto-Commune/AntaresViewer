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
@File       : login.py

@Author     : hsn

@Date       : 2/20/24 6:49 PM
"""
import logging
import uuid
from pathlib import Path
from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm

import src.function.format.avi as AVInfo
from src.function.database.db import DB
from src.toml_config import config
from src.utils.crypto import check_password_hash, JWT

logger = logging.getLogger(__name__)
Name = AVInfo.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
@router.post(default_url)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_agent: Annotated[str | None, Header()] = None):
    # get user
    db = DB(config.DB.db_uri, "Antares_accounts", config.DB.db_username, config.DB.db_password)

    rst = await db.find("users", {"uid": form_data.username})
    if not rst:
        rst = await db.find("users", {"email": form_data.username})
        if not rst:
            raise HTTPException(status_code=400, detail="Incorrect username")

    user_data = rst[0]
    psw_hash = user_data["password"]
    login_success = check_password_hash(password=form_data.password, hash_=psw_hash)

    if login_success:
        with Path("server.key").open("r", encoding="utf-8") as f:
            key = f.read()
        session_id = uuid.uuid4().hex
        token = JWT(key).encode({"uid": form_data.username, "user_agent": user_agent, "session": session_id})

        user_data["active_sessions"][session_id] = user_agent
        await db.update("users", {"uid": form_data.username}, "active_sessions", user_data["active_sessions"])

        return {"code": "200", "access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect password")

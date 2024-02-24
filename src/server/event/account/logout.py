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
@File       : logout.py

@Author     : hsn

@Date       : 2/24/24 2:42 PM
"""
import logging

import fastapi
from fastapi import Depends

import src.function.format.avi as AVInfo
from src.data.containers.user import UserWithSession
from src.utils.oauth import get_current_user

logger = logging.getLogger(__name__)
Name = AVInfo.Name()
default_url = Name.default_url
router = fastapi.APIRouter()


@router.get(default_url)
async def logout(user: UserWithSession = Depends(get_current_user)):
    """
    Logout
    :param user:
    :return:
    """
    print(user.uid)
    user.active_sessions.pop(user.session)
    await user.save()
    return {"code": "200", "message": "Logout successfully."}

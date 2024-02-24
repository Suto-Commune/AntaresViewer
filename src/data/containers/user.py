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
@File       : user.py

@Author     : hsn

@Date       : 2/24/24 2:07 PM
"""
import dataclasses


@dataclasses.dataclass
class User:
    uid: str
    username: str
    password: str
    email: str
    active_sessions: dict = dataclasses.field(default_factory=dict)

    def dump(self):
        return dataclasses.asdict(self)

    @staticmethod
    def load(data: dict):
        return User(**data)


@dataclasses.dataclass
class UserWithSession(User):
    session: str = ''
    user_agent: str = ''

    def set_save_callback(self, callback: callable):
        self.save_callback = callback

    async def save(self):
        if self.save_callback:
            await self.save_callback(self.dump())

    def dump(self):
        d = dataclasses.asdict(self)
        d.pop("session")
        d.pop("user_agent")
        return d

    @staticmethod
    def load(data: dict):
        return UserWithSession(**data)

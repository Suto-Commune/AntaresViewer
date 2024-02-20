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
@File       : crypto.py

@Author     : hsn

@Date       : 2/20/24 8:54 AM
"""
import hashlib
import inspect
import secrets


def _get_hasher(method="sha256"):
    if hasattr(hashlib, method):
        hasher = getattr(hashlib, method)
    else:
        hasher = hashlib.new(method)

    return hasher


def password_hash(
    password: str, method: str = "scrypt", salt_length: int = 16, **kwargs
) -> str:
    """
    Hash the password with the given method.
    :param password: The password to be hashed.
    :param method: The method of hashing to use.See https://docs.python.org/zh-cn/3.10/library/hashlib.html.
    :param salt_length: The length of the salt to be used.
    :param kwargs: The parameters of the hasher.
    :return: hashed password.
    """
    # generate the salt
    salt = secrets.token_bytes(salt_length)

    # get the hasher
    hasher = _get_hasher(method)

    # hash the password
    hash_ = hasher(password.encode("utf-8"), salt=salt, **kwargs).hex()

    # get the parameters of the hasher
    #   The purpose of this paragraph is to ensure that the data is stored in the correct order and that the parameters
    #   are not duplicated. Where, in 'filter', 'lambda x: x not in ['salt', 'password']` is used to exclude duplicate
    #   arguments. `kwargs.get(i, parameters[i].default)` is to ensure that the default value is used instead of
    #   reporting an error if the parameter cannot be found.
    parameters = inspect.signature(hasher).parameters
    sorted_parameters = sorted(
        filter(lambda x: x not in ["salt", "password"], parameters.keys())
    )
    data_list = (str(kwargs.get(i, parameters[i].default)) for i in sorted_parameters)

    # return the hash
    return f'{method}${salt.hex()}${"$".join(data_list)}${hash_}'


def check_password_hash(password: str, hash_: str) -> bool:
    """
    Check if the password matches the hash.
    :param password:
    :param hash_:
    :return:
    """
    # unpack the hash to pure_hash and parameters
    method, salt, *params, hash__ = hash_.split("$")

    # get the hasher
    hasher = _get_hasher(method)

    # get the parameters of the hasher
    p = inspect.signature(hasher).parameters
    sp = sorted(
        filter(lambda x: x not in ["salt", "password"], map(lambda x: x[0], p.items()))
    )
    kwarg = {k: int(v) for k, v in zip(sp, params)}

    # hash the password
    h = hasher(password.encode("utf-8"), salt=bytes.fromhex(salt), **kwarg).hex()

    # return the result
    return h == hash__

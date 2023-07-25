#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. Suto-Commune
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : main.py

@Author     : Natsumi

@Date       : 2023/7/25 0:00
"""
import logging
from src.server import Server

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s][%(filename)s] %(message)s',
                    datefmt='%b/%d/%Y-%H:%M:%S')
logger = logging.getLogger(__name__)


def info():
    logger.info("AntaresViewer 2023@Suto-Commune")


if __name__ == "__main__":
    info()
    server = Server()
    server.launcher()

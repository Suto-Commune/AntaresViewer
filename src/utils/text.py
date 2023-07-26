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
@File       : text.py

@Author     : hsn

@Date       : 7/26/23 10:47 AM
"""
import copy
import re
from typing import Generator, Any, Iterable


def get_contents(text: str) -> list[dict[str, list | str]]:
    """
    Get the contents of a text.
    :param text: The text to get contents.
    :return: The contents of the text.
    """
    return list(_recursive_fetching_of_chapters(
        text,
        ['丛', '系', '卷', '部', '本', '册', '篇', '编', '回', '话', '章', '节',
         '']
    ))


def _recursive_fetching_of_chapters(
        text: str,
        tl: list[str]) -> Generator[dict[str, list | str], None, None]:
    """
    Fetch the chapters of a text recursively.
    :param text: The text to fetch chapters.
    :param tl: The title list.
    :return: The chapters of the text.
    """
    if not tl:
        return
    t = tl.pop(0)
    chapter_iter = re_search_all_iter(rf'\n *[第]?[0123456789一二三四五六七八九十零〇百千两]+{t} *\n', text)  # 1, 2, 3
    chapter_iter1 = re_search_all_iter(rf'\n *[第]?[0123456789一二三四五六七八九十零〇百千两]+{t} +\S{{1,24}}',
                                       text)  # 1 xxx, 2 yyy, 3 zzz
    chapter_iter2 = re_search_all_iter(rf'\n.{{,6}}[第]?[0123456789一二三四五六七八九十零〇百千两]+{t}\s+\S{{1,24}}',
                                       text)
    chapter_iter_list = [chapter_iter, chapter_iter1, chapter_iter2]

    def set_content_pos(_iterable: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        last_v = None
        v = None
        for _i, v in enumerate(_iterable):
            if last_v:
                yield {**last_v, 'content_pos': (last_v['title_pos'][1], v['title_pos'][0])}
            last_v = v
        if v:
            yield {**v, 'content_pos': (v['title_pos'][1], len(text))}

    def temp(_chapter_iter: Generator[dict[str, Any], None, None]) -> Generator[dict[str, Any], None, None]:
        for _i in set_content_pos(
                {'title_pos': __i['span'], 'name': __i['group'], 'inner': []} for __i in _chapter_iter):
            _i['inner'] = list(
                _recursive_fetching_of_chapters(text[_i['content_pos'][0]:_i['content_pos'][1]], copy.deepcopy(tl)))
            yield _i

    for i in chapter_iter_list:
        if rt := list(temp(i)):
            yield from rt
            break
    else:
        yield from _recursive_fetching_of_chapters(text, tl)


def re_search_all_iter(pattern: str, text: str) -> Generator[dict[str, str | tuple], None, None]:
    """
    Search all matches of a pattern in a text.
    :param pattern: The pattern to search.
    :param text: The text to search.
    :return: The matches of the pattern in the text.
    """
    last = 0
    while _next := re.search(pattern, text):
        span_start, span_end = _next.span()

        yield {'span': (span_start + last, span_end + last), 'group': _next.group()}
        last += span_end
        text = text[_next.end():]

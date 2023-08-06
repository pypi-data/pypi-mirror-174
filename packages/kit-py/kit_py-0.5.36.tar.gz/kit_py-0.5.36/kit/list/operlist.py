# -*- coding: utf-8 -*-
from typing import Generator, List


def split_list_average_n(origin_list: List, n: int) -> Generator[List, None, None]:
    """
    按指定数量平均分割列表
    :param origin_list: 原始列表
    :param n: 指定数量
    :return: 分割后的列表

    >>> list(split_list_average_n([1, 2, 3, 4, 5, 6, 7, 8, 9], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]

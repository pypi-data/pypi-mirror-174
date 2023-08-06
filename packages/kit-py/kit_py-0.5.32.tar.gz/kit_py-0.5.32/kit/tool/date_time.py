# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def get_timestamp() -> int:
    """
    获取10位当前时间戳
    :return: 时间戳
    """
    return int(datetime.now().timestamp())


def get_timestamp13() -> int:
    """
    获取13位当前时间戳
    :return: 时间戳
    """
    return int(datetime.now().timestamp() * 1000)


def get_now(fmt=None) -> str:
    """
    获取当前时间
    :param fmt: 时间格式
    :return: 时间
    """
    _fmt = fmt or '%Y-%m-%d %H:%M:%S'
    return datetime.now().strftime(_fmt)


def get_before_time(num, unit=None, fmt=None):
    """
    获取当前时间之前的时间
    :param num: 数量
    :param unit: 单位
    :param fmt: 时间格式
    :return: 时间
    """
    _fmt = fmt or '%Y-%m-%d %H:%M:%S'
    _unit = unit or 'days'
    return (datetime.now() - timedelta(**{_unit: num})).strftime(_fmt)


if __name__ == '__main__':
    print(get_timestamp())
    print(get_timestamp13())
    print(get_before_time(30, 'days'))
    # 1639656228

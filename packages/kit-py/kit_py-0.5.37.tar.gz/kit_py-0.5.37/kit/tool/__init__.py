# -*- coding: utf-8 -*-
from uuid import uuid4
from .import_object import import_object
from .current_platform import current_platform
from .date_time import get_timestamp, get_timestamp13
from .random_useragent import get_useragent

__all__ = [
    'cookies_to_dict',
    'headers_to_dict',
    'data_to_dict',
    'import_object',
    'current_platform',
    'get_timestamp',
    'get_timestamp13',
    'get_useragent',
    'gen_unique_id'
]


def cookies_to_dict(cookies: str):
    return {cookie.split('=')[0]: cookie.split('=')[-1] for cookie in cookies.split('; ')}


def headers_to_dict(headers: str) -> dict:
    return {header.split(':')[0]: header.split(':')[-1] for header in headers.split('\r\n')}


def data_to_dict(data: str) -> dict:
    return {item.split('=')[0]: item.split('=')[-1] for item in data.split('&')}


def gen_unique_id():
    return f"{uuid4().hex}"


if __name__ == '__main__':
    gen_unique_id()

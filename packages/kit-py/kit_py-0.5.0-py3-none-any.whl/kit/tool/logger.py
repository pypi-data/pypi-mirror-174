# -*- coding: utf-8 -*-
import json
import logging
from logging.handlers import SocketHandler
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def __init__(self, app):
        super(JsonFormatter, self).__init__()
        self.app = app

    def formatException(self, exc_info):
        exc_text = super(JsonFormatter, self).formatException(exc_info)
        return repr(exc_text)

    def format(self, record):
        message = {
            "app": self.app,
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.format_timestamp(record.created)
        }
        message.update(self.get_extra_info(record))
        if record.exc_text and 'trace' not in message:
            message['trace'] = f"{record.exc_text}"
        return json.dumps(message)

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.fromtimestamp(time)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @classmethod
    def get_extra_info(cls, record):
        skip_list = ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 'module', 'exc_info',
                     'exc_text',
                     'stack_info', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
                     'processName', 'process']
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in skip_list
        }


class LogstashHandler(SocketHandler):

    def __init__(self, host, port, formatter=None):
        super(LogstashHandler, self).__init__(host, port)
        self.formatter = formatter

    def makePickle(self, record):
        return bytes(self.formatter.format(record) + '\n', 'utf-8')

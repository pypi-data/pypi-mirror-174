# -*- coding: utf-8 -*-
import json
import logging
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
            "timestamp": self.format_timestamp(record.created)
        }
        message.update(self.get_extra_info(record))

        if record.exc_info:
            message['message'] = self.formatException(record.exc_info)
            message['trace'] = record.getMessage()
        else:
            message['message'] = record.getMessage()

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


class LogstashHandler(logging.StreamHandler):

    def __init__(self, formatter=None):
        super().__init__()
        self.formatter = formatter

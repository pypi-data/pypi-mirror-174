# -*- coding: utf-8 -*-
from rpc.middleware.middleware import Middleware


class TestMiddleware(Middleware):

    def before_send(self, broker, message, *args, **kwargs):
        print("before_send", message)

    def after_send(self, broker, message, *args, **kwargs):
        print("after_send", message)

    def before_process_message(self, broker, message, *args, **kwargs):
        # do something
        message.error = True
        print("before_process_message", message)

    def after_process_message(self, broker, message, result, *args, **kwargs):
        print("after_process_message", message, result)
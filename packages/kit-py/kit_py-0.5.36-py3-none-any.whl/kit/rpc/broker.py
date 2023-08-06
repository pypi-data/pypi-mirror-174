# -*- coding: utf-8 -*-
from .store import get_store


class Broker:

    def __init__(self, queue, backend_store=None, middlewares=None):
        self.backend_store = backend_store or self._get_default_store()
        self.queue = queue
        self.middlewares = []
        self.job = None

        if middlewares:
            for middleware in middlewares:
                self.add_middleware(middleware)

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def send(self, message):
        self.backend_store.send(self.queue, message)

    def consume(self, *args, **kwargs):
        return self.backend_store.consume(self.queue, *args, **kwargs)

    def before_emit(self, signal, *args, **kwargs):
        signal = "before_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    def after_emit(self, signal, *args, **kwargs):
        signal = "after_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    def _get_default_store(self):
        return get_store()

    def __repr__(self):
        return f"<Broker {self.queue}>"

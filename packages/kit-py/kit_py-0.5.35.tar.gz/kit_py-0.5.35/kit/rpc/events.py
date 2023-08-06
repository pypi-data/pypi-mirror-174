# -*- coding: utf-8 -*-
class Events:

    def __init__(self):
        self._events = {}

    def on(self, event, fn):
        self._events.setdefault(event, []).append(fn)

    def emit(self, event, **kwargs):
        if not event.startswith('on_'):
            event = f'on_{event}'
        for fn in self._events.get(event, []):
            fn(**kwargs)

    def remove(self, event, fn):
        self._events.get(event, []).remove(fn)

    def all(self):
        return self._events


events = Events()

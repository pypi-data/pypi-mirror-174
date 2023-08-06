# -*- coding: utf-8 -*-
import time


class time_cache:   # noqa

    def __init__(self, ttl):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            last_call_time = self.cache.get('last_call_time', time.time())

            if int(time.time() - last_call_time) < self.ttl and key in self.cache:
                return self.cache[key]
            else:
                self.cache[key] = fn(*args, **kwargs)
                self.cache['last_call_time'] = time.time()
                return self.cache[key]

        return wrapper


class count_cache:   # noqa

    def __init__(self, count):
        self.count = count
        self.cache = {}

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            use_count = self.cache.get('count', 0)
            if use_count < self.count - 1 and key in self.cache:
                self.cache['count'] += 1
                return self.cache[key]
            else:
                self.cache[key] = fn(*args, **kwargs)
                self.cache['count'] = 0
                return self.cache[key]

        return wrapper

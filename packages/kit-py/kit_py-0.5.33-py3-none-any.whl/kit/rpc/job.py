# -*- coding: utf-8 -*-
import logging
import json
from inspect import isgenerator

from .broker import Broker
from .message import Message
from .worker import _ConsumerThread

from .events import events as _events
from kit.tool import gen_unique_id

logger = logging.getLogger(__name__)


class Job:

    def __init__(self,
                 fn,
                 job_id=None,
                 from_broker=None, to_broker=None,
                 config=None):
        self.fn = fn
        self.job_id = job_id or gen_unique_id()
        self.from_broker = from_broker
        self.to_broker = to_broker
        self.config = config
        if self.from_broker:
            self.from_broker.job = self
            self._add_consumer()
        _events.emit("job_init", job=self)

    def send(self, message, broker=None):
        if message is None:
            logger.debug("send message is None")
            return
        if self.to_broker is None and broker is None:
            logger.debug("send broker is None")
            return
        _broker = broker or self.to_broker

        try:
            _config = self._get_config(_broker)
        except Exception as e:
            logger.warning(f"Failed to get config: {e}")
            _config = {}
        message = Message(message)

        # 外部的配置优先级高于内部的配置
        kwargs = {**_config, **(message.message.get("kwargs", {}) or {})}
        message.message['kwargs'] = kwargs
        self._post_message(_broker, message)

    def _post_message(self, broker, message):
        _events.emit("job_send", job=self, broker=broker, message=message)
        broker.before_emit("send", message=message)
        if not message.failed:
            broker.send(message.asstr())
        broker.after_emit("send", message=message)

    def _add_consumer(self):
        _events.emit("job_add_consumer", job=self, broker=self.from_broker)
        consumer = _ConsumerThread(
            fn=self,
            broker=self.from_broker,
            prefetch=1,
            worker_timeout=1000
        )
        consumer.start()

    def _get_config(self, broker: Broker):
        if not self.config:
            return {}

        if not (cfg := self.config.get(broker.queue)):
            return {}

        try:
            return json.loads(cfg)
        except json.JSONDecodeError:
            return {}

    def __call__(self, *args, **kwargs):
        """当作为函数调用时，执行fn"""
        res = self.fn(*args, **kwargs)
        if isgenerator(res):
            for item in res:
                self.send(item)
        else:
            self.send(res)
        return res

    def __repr__(self):
        return f"<Job {self.job_id}>"


class JobMixin:

    def job(self,
            job_class=Job,
            job_id=None,
            from_broker=None,
            to_broker=None,
            config=None):
        """
        任务装饰器
        :param job_class: 任务类
        :param job_id: 任务id
        :param from_broker: 从哪个broker消费
        :param to_broker: 发送到哪个broker
        :param config: 配置中心
        :return:
        """

        def decorator(fn):
            return job_class(fn,
                             job_id=job_id,
                             from_broker=from_broker,
                             to_broker=to_broker,
                             config=config)

        return decorator

    def register_events(self, **events):
        for name, event in events.items():
            _events.on(name, event)

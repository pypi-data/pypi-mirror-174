# -*- coding: utf-8 -*-
import logging
import time
from threading import Thread, Event

from .message import AMQPMessage
from .events import events

logger = logging.getLogger(__name__)


class _ConsumerThread(Thread):

    def __init__(self, fn, broker, prefetch, worker_timeout):
        super().__init__(daemon=True)
        self.job_callback = fn
        self.running = False
        self.consumer = None
        self.broker = broker
        self.paused = False
        self.paused_event = Event()
        self.prefetch = prefetch
        self.worker_timeout = worker_timeout

    def run(self):
        self.running = True
        while self.running:
            if self.paused:
                self.paused_event.set()
                time.sleep(self.worker_timeout / 1000)
                continue

            self.consumer = self.broker.consume(
                prefetch=self.prefetch,
                timeout=self.worker_timeout,
            )
            for message in self.consumer:
                if message:
                    message = AMQPMessage(message)
                    events.emit('on_receive', job=self.job_callback, message=message)
                    self.broker.before_emit("callback", message=message)
                    result = self._run_job_callback(message)
                    self.broker.after_emit("callback", message=message, result=result)

    def _run_job_callback(self, message):
        """
        job_callback(message=message.message, amqp_message=message)
        message:
            为了下游接收到的直接是MQ中的消息，而不是AMQPMessage对象，提前解构出来
        options:
            从message中解构出来，方便下游使用
        """
        try:
            res = self.job_callback(message=message.message, options=message.options)
        except Exception as e:
            logger.debug(f'Failed to run fn: {e}')
            events.emit('on_job_error', job=self.job_callback, message=message, error=e)
            self.consumer.nack(message.amqp_message)
            return
        self.consumer.ack(message.amqp_message)
        return res

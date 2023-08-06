# -*- coding: utf-8 -*-
import logging
from threading import local
from typing import Optional, List, Dict, Union

import pika
import pika.exceptions

MAX_SEND_ATTEMPTS = 6  # 最大发送重试次数

logger = logging.getLogger(__name__)


class RabbitmqStore:

    def __init__(self, *, confirm_delivery=False, max_priority=None,
                 url: Union[str, List[str], None] = None,
                 parameters: Optional[List[Dict]] = None,
                 **kwargs):
        """
        :param url: RabbitMQ URL
        :param parameters: RabbitMQ parameters
        :param kwargs: RabbitMQ parameters
        .. parameters docs: https://pika.readthedocs.io/en/stable/modules/parameters.html
        """
        if max_priority is not None and not (0 < max_priority <= 255):
            raise ValueError("max_priority must be a value between 0 and 255")

        if url is not None:
            if parameters is not None:
                raise ValueError("url and parameters are mutually exclusive")

            if isinstance(url, str) and ';' in url:
                self.parameters = [pika.URLParameters(u) for u in url.split(';')]
            elif isinstance(url, list):
                self.parameters = [pika.URLParameters(u) for u in url]
            else:
                self.parameters = pika.URLParameters(url)
        elif parameters is not None:
            self.parameters = [pika.ConnectionParameters(**p) for p in parameters]
        else:
            self.parameters = pika.ConnectionParameters(**kwargs)

        self.confirm_delivery = confirm_delivery
        self.max_priority = max_priority
        self.state = local()

    @property
    def connection(self):
        connection = getattr(self.state, "connection", None)
        if connection is None:
            connection = self.state.connection = pika.BlockingConnection(
                parameters=self.parameters)
        return connection

    @connection.deleter
    def connection(self):
        del self.channel
        try:
            connection = self.state.connection
        except AttributeError:
            return

        del self.state.connection
        if connection.is_open:  # noqa
            try:
                connection.close()
            except Exception as e:
                logger.debug(f"Encountered exception while closing Connection.{e}")

    @property
    def channel(self):
        channel = getattr(self.state, "channel", None)
        if channel is None:
            channel = self.state.channel = self.connection.channel()
            if self.confirm_delivery:
                channel.confirm_delivery()
        return channel

    @channel.deleter
    def channel(self):
        try:
            channel = self.state.channel
        except AttributeError:
            return

        del self.state.channel
        if channel.is_open:  # noqa
            try:
                channel.close()
            except Exception as e:
                logger.debug(f"Encountered exception while closing Channel.{e}")

    @property
    def consumer_class(self):
        return _RabbitmqConsumer

    def consume(self, queue_name, prefetch=1, timeout=5000):
        self.declare_queue(queue_name)
        return self.consumer_class(self.parameters, queue_name, prefetch, timeout)

    def close(self):
        """关闭连接"""
        try:
            self.channel.close()
            self.connection.close()
        except pika.exceptions.AMQPError:
            pass
        except Exception as e:
            logger.debug(f"Encountered exception while closing Channel.{e}")

    def declare_queue(self, queue_name, arguments=None):
        """声明队列"""
        if arguments is None:
            arguments = {}
        if self.max_priority is not None:
            arguments["x-max-priority"] = self.max_priority
        return self.channel.queue_declare(queue=queue_name, durable=True, arguments=arguments)

    def get_message_counts(self, queue_name):
        """获取消息数量"""
        queue_response = self.declare_queue(queue_name)
        return queue_response.method.message_count

    def flush_queue(self, queue_name):
        """清空队列"""
        self.channel.queue_purge(queue_name)

    def send(self, queue_name, body, priority=None, properties=None):
        """发送消息"""
        self.declare_queue(queue_name)

        if properties is None:
            properties = pika.BasicProperties()
        if priority is not None:
            properties.priority = priority
        attempts = 1
        while True:
            try:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    body=body, properties=properties)
                return body
            except (pika.exceptions.AMQPConnectionError,
                    pika.exceptions.AMQPChannelError) as exc:

                del self.connection
                attempts += 1
                if attempts > MAX_SEND_ATTEMPTS:
                    raise exc


class _RabbitmqConsumer:

    def __init__(self, parameters, queue_name, prefetch, timeout):
        try:
            self.connection = pika.BlockingConnection(parameters=parameters)
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=prefetch)
            self.iterator = self.channel.consume(queue_name, inactivity_timeout=timeout / 1000)
        except (pika.exceptions.AMQPConnectionError,
                pika.exceptions.AMQPChannelError) as e:
            raise e

    def ack(self, message):
        try:
            self.channel.basic_ack(message.tag)
        except (pika.exceptions.AMQPConnectionError,
                pika.exceptions.AMQPChannelError) as e:
            raise e
        except Exception as e:
            logger.debug('ack error: {}'.format(e))

    def nack(self, message, requeue=False):
        try:
            self._nack(message.tag, requeue=requeue)
        except (pika.exceptions.AMQPConnectionError,
                pika.exceptions.AMQPChannelError) as e:
            raise e
        except Exception as e:
            logger.debug('nack error: {}'.format(e))

    def _nack(self, tag, requeue=False):
        self.channel.basic_nack(tag, requeue=requeue)

    def __next__(self):
        try:
            method, properties, body = next(self.iterator)
            if method is None:
                return None
        except (AssertionError,
                pika.exceptions.AMQPConnectionError,
                pika.exceptions.AMQPChannelError) as e:
            raise e
        try:
            _message = body.decode("utf-8")
        except Exception as e:
            logger.exception('decode error: {}'.format(e))
            self._nack(method.delivery_tag)
            return None
        rmq_message = _RabbitmqMessage(
            method.redelivered,
            method.delivery_tag,
            _message
        )
        return rmq_message

    def __iter__(self):  # pragma: no cover
        return self


class _RabbitmqMessage:
    def __init__(self, redelivered, tag, message):
        self.redelivered = redelivered
        self.tag = tag
        self.message = message

    def __repr__(self):
        return '<RabbitmqMessage: {}>'.format(self.message)


if __name__ == '__main__':
    rmq = RabbitmqStore(url='amqp://admin:admin@localhost:5672/%2F')
    # rmq.send('test', '22')
    print(rmq.get_message_counts('job.stuff'))

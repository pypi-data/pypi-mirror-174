# -*- coding: utf-8 -*-
import logging

from ..broker import Broker
from .middleware import Middleware

logger = logging.getLogger(__name__)


class TransferMiddleware(Middleware):
    """"将消息转发给指定app_name的broker"""

    def before_callback(self, broker, message, *args, **kwargs):

        logger.info('start transfer message', extra={'broker': broker.queue})
        try:
            to_broker = Broker(message.message.app_name)
            broker.job.send(message=message.message, broker=to_broker)
        except Exception as e:
            logger.error(f'Failed to transfer message: {e}')

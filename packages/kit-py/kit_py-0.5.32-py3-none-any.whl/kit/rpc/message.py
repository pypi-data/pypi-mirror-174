# -*- coding: utf-8 -*-
import logging
import json
from dataclasses import dataclass, field
from typing import Any

from amqpstorm.message import Message as AmqpMessage
from kit.dict import Dict

logger = logging.getLogger(__name__)


@dataclass
class MessageSchema:
    message: Any
    options: dict = field(default_factory=dict)


class AMQPMessage:

    def __init__(self, message: AmqpMessage):
        self._message = message
        self.options = Dict()

    @property
    def amqp_message(self):
        return self._message

    @property
    def body(self):
        return self._message.body

    @property
    def message_id(self):
        return self._message.message_id

    @property
    def delivery_tag(self):
        return self._message.delivery_tag

    @property
    def message(self):
        try:
            return Dict(json.loads(self.body))
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode message: {self.body}")
            return {}


class Message:

    def __init__(self, message: Any):
        self.message = Dict(message)
        self.failed = False

    def asdict(self):
        return self.message

    def asstr(self):
        return json.dumps(self.message)

    def fail(self):
        self.failed = True

    def __repr__(self):
        return f"<Message: {self.message}>"

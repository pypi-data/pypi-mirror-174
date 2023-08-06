import pickle
from typing import Callable

import pika
from loguru import logger

from vidis_algorithms_api.models import Payload


def parse_body_and_callback(ch, method, properties, body, callback: Callable):
    try:
        payload_dict = pickle.loads(body)
        payload = Payload(**payload_dict)
        callback(payload)
    except Exception as e:
        logger.exception(e)


class Consumer:
    def __init__(self, rabbit_url: str = 'ampq://localhost'):
        self.connection_parameters = pika.URLParameters(rabbit_url)

    def loop(self, channel_name: str, callback: Callable):
        try:
            connection = pika.BlockingConnection(self.connection_parameters)
            channel = connection.channel()
            channel.queue_declare(queue=channel_name)
            channel.basic_consume(queue=channel_name, auto_ack=True,
                                  on_message_callback= \
                                      lambda ch, method, properties, body: parse_body_and_callback(ch,
                                                                                                   method,
                                                                                                   properties,
                                                                                                   body,
                                                                                                   callback))
            channel.start_consuming()
        except Exception as e:
            logger.exception(e)
        finally:
            try:
                channel.close()
                connection.close()
            finally:
                pass

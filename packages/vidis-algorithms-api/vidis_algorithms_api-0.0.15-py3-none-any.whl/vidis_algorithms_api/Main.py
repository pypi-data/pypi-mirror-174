from loguru import logger

from MQConsumer import Consumer
from vidis_algorithms_api.models import Payload


def callback(payload: Payload):
    try:
        logger.info(payload.dict())
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    consumer = Consumer('amqp://guest:guest@localhost:5672')
    consumer.loop('test', callback)

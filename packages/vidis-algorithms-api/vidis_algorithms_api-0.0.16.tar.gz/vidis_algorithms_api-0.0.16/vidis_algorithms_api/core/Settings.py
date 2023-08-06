import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_PATH = os.environ.get('DATA_PATH', './data')

    MARIA_CONNECTOR: str = 'mariadb+mariadbconnector'
    MARIA_USERNAME: str = 'root'
    MARIA_PASSWORD: str = 'qwerty322'
    MARIA_URL: str = 'db'
    MARIA_PORT: str = '3306'
    MARIA_SCHEMA: str = 'main'
    MARIA_DB_ADDRESS = f'{MARIA_CONNECTOR}://{MARIA_USERNAME}:{MARIA_PASSWORD}@{MARIA_URL}:{MARIA_PORT}/{MARIA_SCHEMA}'

    AMQP_ADDRESS = os.environ.get('AMQP_ADDRESS', 'amqp://guest:guest@localhost:5672')

    TASK_DATE_FORMAT = '%d/%m/%y %H:%M:%S'
    DATA_FOLDER_NAME = '%d_%m_%Y%H_%M_%S_%f'

    CUSTOM_LAYER_FOLDER = 'custom_algorithm'

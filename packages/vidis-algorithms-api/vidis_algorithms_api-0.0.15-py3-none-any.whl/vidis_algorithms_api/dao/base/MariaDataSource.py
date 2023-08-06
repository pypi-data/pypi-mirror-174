from contextlib import contextmanager

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vidis_algorithms_api.core import settings
from vidis_algorithms_api.dao.base.SQLDataSource import SQLDataSource


class MariaDataSource(SQLDataSource):
    def __init__(self):
        self.session_factory = None
        self.engine = None
        self.create_connection()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MariaDataSource, cls).__new__(cls)
        return cls.instance

    def create_connection(self):
        try:
            database_url = settings.MARIA_DB_ADDRESS
            self.engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
            self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        except Exception as e:
            logger.exception(f"The error '{e}' is occurred")

    @contextmanager
    def get_session(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.exception(e)
            session.rollback()
            raise
        finally:
            session.close()

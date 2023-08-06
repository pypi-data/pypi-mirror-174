from abc import ABC, abstractmethod, ABCMeta


class Singleton(ABCMeta):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SQLDataSource(ABC, metaclass=Singleton):
    @abstractmethod
    def create_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_session(self, *args, **kwargs):
        pass

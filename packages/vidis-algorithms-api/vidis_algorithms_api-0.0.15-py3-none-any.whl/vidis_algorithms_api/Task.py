import os.path
from abc import abstractmethod, ABC
from datetime import datetime

import numpy as np
from loguru import logger

from vidis_algorithms_api import Consumer
from vidis_algorithms_api.core import settings
from vidis_algorithms_api.dao import AsyncTaskDao
from vidis_algorithms_api.dao import CustomLayerDao
from vidis_algorithms_api.models import Payload
from vidis_algorithms_api.utils import DataProvider


class Status:
    PENDING: str = 'PENDING'
    STARTED: str = 'STARTED'
    SUCCESS: str = 'SUCCESS'
    FAILURE: str = 'FAILURE'


class Task(ABC):
    TASK_DAO = AsyncTaskDao()
    COMPUTED_LAYER_DAO = CustomLayerDao()
    DATA_PROVIDER = DataProvider()

    def _set_end_time(self):
        end_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        self.TASK_DAO.set_end_time_by_task_id(self.id, end_time)

    def _set_task_status(self, status):
        self.TASK_DAO.set_task_status(self.id, status)

    def _save_task_result(self, payload: Payload, layer_data: np.ndarray):
        self.COMPUTED_LAYER_DAO.insert_custom_layer(payload.name, self.get_type_name(), payload.id,
                                                    payload.params if payload.params is not None else {})
        path_to_save = os.path.join(os.path.dirname(payload.path), settings.CUSTOM_LAYER_FOLDER, payload.name + '.npy')
        np.save(path_to_save, layer_data)

    @abstractmethod
    def run(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        pass

    @abstractmethod
    def get_type_name(self) -> str:
        """
        Should return plain string contains a name of the algorithm.
        Just try not to use names which may already be taken (e.g. pca, kmeans)
        :return:
        """
        pass

    def __call__(self, payload: Payload):
        self.id = payload.id
        self._set_task_status(Status.STARTED)
        hyperspecter = self.DATA_PROVIDER.get_specter(payload.path)
        try:
            result = self.run(hyperspecter, **payload.params)
            if len(result) == 0:
                raise Exception('Empty result returned from algorithm module')
            self._set_task_status(Status.SUCCESS)
            self._save_task_result(payload, result)
        except Exception as e:
            logger.exception(e)
            self._set_task_status(Status.FAILURE)
        finally:
            self._set_end_time()
            pass

    def serve(self):
        consumer = Consumer(settings.AMQP_ADDRESS)
        consumer.loop(self.get_type_name(), lambda payload: self(payload))

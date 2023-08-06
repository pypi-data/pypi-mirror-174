from vidis_algorithms_api.dao.base import MariaDataSource
from vidis_algorithms_api.models import AsyncTask


class AsyncTaskDataSource(MariaDataSource):

    def __init__(self):
        super().__init__()
        self.create_connection()

    def set_end_time_by_task_id(self, task_id, end_time):
        with self.get_session() as sess:
            sess.query(AsyncTask).filter(AsyncTask.task_id == task_id).update({AsyncTask.end_time: end_time})

    def set_specter_id_by_task_id(self, task_id, specter_id):
        with self.get_session() as sess:
            sess.query(AsyncTask).filter(AsyncTask.task_id == task_id).update({AsyncTask.specter_id: specter_id})

    def set_task_status(self, task_id: str, task_status: str):
        with self.get_session() as sess:
            sess.query(AsyncTask).filter(AsyncTask.task_id == task_id).update({AsyncTask.status: task_status})

    def set_task_result(self, task_id: str, task_result: str):
        """
        :param task_result: should be json string
        """
        with self.get_session() as sess:
            task = sess.query(AsyncTask).get(task_id)
            task.task_result = task_result

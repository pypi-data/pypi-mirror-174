from vidis_algorithms_api.dao.datasources import AsyncTaskDataSource


class AsyncTaskDao:
    """
    Give access to AsyncTask and UserSession (ain't use it now) CRUD methods
    """

    def __init__(self):
        self.data_source = AsyncTaskDataSource()

    def set_end_time_by_task_id(self, task_id: str, end_time: str):
        self.data_source.set_end_time_by_task_id(task_id, end_time)

    def set_specter_id_by_task_id(self, task_id: str, specter_id: int):
        self.data_source.set_specter_id_by_task_id(task_id, specter_id)

    def set_task_result(self, task_id: str, task_result: str):
        self.data_source.set_task_result(task_id, task_result)

    def set_task_status(self, task_id: str, task_status: str):
        self.data_source.set_task_status(task_id, task_status)

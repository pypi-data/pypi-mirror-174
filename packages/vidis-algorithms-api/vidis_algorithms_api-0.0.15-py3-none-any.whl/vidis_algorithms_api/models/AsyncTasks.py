import json

from sqlalchemy import Column, String

from vidis_algorithms_api.models import Base


class AsyncTask(Base):
    __tablename__ = 'AsyncTask'

    task_id = Column(String(length=100), primary_key=True)
    username = Column(String(length=100), nullable=False)
    task_type = Column(String(length=100), nullable=False)
    task_name = Column(String(length=100), nullable=False)
    specter_id = Column(String(length=100), nullable=False)
    start_time = Column(String(length=100), nullable=False)
    end_time = Column(String(length=100))
    status = Column(String(length=20), default='PENDING')
    task_result = Column(String(length=5_000), default='{}')

    @staticmethod
    def from_dict(_json: dict):
        obj = AsyncTask()
        for key in _json:
            setattr(obj, key, _json[key])
        return obj

    def as_dict(self):
        return {
            'task_id': self.task_id,
            'username': self.username,
            'task_type': self.task_type,
            'task_name': self.task_name,
            'specter_id': self.specter_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'task_result': json.loads(self.task_result) if self.task_result is not None else {}
        }

    def __repr__(self):
        return f'<AsyncTask({self.username}, {self.task_id})>'




from sqlalchemy import Integer, Column, String, ForeignKey

from vidis_algorithms_api.models import Base, Hyperspecter


class CustomLayer(Base):
    __tablename__ = 'CustomLayer'

    id = Column(Integer, autoincrement=True, primary_key=True)
    specterId = Column(Integer, ForeignKey(Hyperspecter.id, ondelete='CASCADE'))
    name = Column(String(length=100), nullable=False)
    type = Column(String(length=100), nullable=True)
    params = Column(String(length=500), nullable=True)

    @staticmethod
    def from_dict(_json: dict):
        obj = CustomLayer()
        for key in _json:
            setattr(obj, key, _json[key])
        return obj

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'specterId': self.specterId,
            'params': self.params
        }

    def __repr__(self):
        return f'<CustomLayer({self.name=}, {self.type=}, {self.specterId=})>'

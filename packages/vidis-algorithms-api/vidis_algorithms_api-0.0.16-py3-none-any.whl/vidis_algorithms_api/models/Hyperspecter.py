from sqlalchemy import Integer, Column

from vidis_algorithms_api.models import Base


class Hyperspecter(Base):
    __tablename__ = 'Hyperspecter'
    id = Column(Integer, primary_key=True, autoincrement=True)

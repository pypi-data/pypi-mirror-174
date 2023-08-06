from vidis_algorithms_api.dao.base import MariaDataSource
from vidis_algorithms_api.models import CustomLayer


class CustomLayerDataSource(MariaDataSource):

    def __init__(self):
        super().__init__()
        self.create_connection()

    def insert_layer(self, layer: CustomLayer):
        with self.get_session() as sess:
            sess.add(layer)

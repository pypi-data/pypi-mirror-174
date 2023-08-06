from vidis_algorithms_api.dao.datasources import CustomLayerDataSource
from vidis_algorithms_api.models import CustomLayer

from json import dumps


class CustomLayerDao:

    def __init__(self):
        self.data_source = CustomLayerDataSource()

    def insert_custom_layer(self, name: str, type: str, specter_id: str, params: dict):
        layer = CustomLayer.from_dict({"name": name, type: "type", "specterId": specter_id, "params": dumps(params)})
        self.data_source.insert_layer(layer)

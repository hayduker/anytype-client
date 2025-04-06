from .api import apiEndpoints
from .object import Object


class ListView:
    def __init__(self):
        self._apiEndpoints: apiEndpoints | None = None
        self.space_id = ""
        self.list_id = ""
        self.id = ""
        self.name = ""

    def get_objectsinlistview(self, offset=0, limit=100):
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        response_data = self._apiEndpoints.getObjectsInList(
            self.space_id, self.list_id, self.id, offset, limit
        )

        results = []
        for data in response_data.get("data", []):
            new_item = Object()
            new_item._apiEndpoints = self._apiEndpoints
            for key, value in data.items():
                new_item.__dict__[key] = value
            results.append(new_item)
        return results

    def add_objectsinlistview(self, objs: list[Object]) -> None:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        id_lists = [obj.id for obj in objs]
        self._apiEndpoints.addObjectsToList(self.space_id, self.list_id, id_lists)

    def delete_objectinlistview(self, obj: Object) -> None:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        self._apiEndpoints.deleteObjectsFromList(self.space_id, self.list_id, obj.id)

    def __repr__(self):
        return f"<ListView(name={self.name})>"

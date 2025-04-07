import pytest
from anytype.listview import ListView
from anytype.object import Object

import pytest
from anytype.listview import ListView
from anytype.object import Object


class DummyAPI:
    def getObjectsInList(self, space_id, list_id, view_id, offset, limit):
        return {"data": [{"id": "1", "name": "Test"}]}

    def addObjectsToList(self, space_id, list_id, ids):
        assert isinstance(ids, list)

    def deleteObjectsFromList(self, space_id, list_id, obj_id):
        assert isinstance(obj_id, str)


def test_repr_listview():
    lv = ListView()
    lv.name = "Tasks"
    assert repr(lv) == "<ListView(name=Tasks)>"


def test_listview_auth_required():
    lv = ListView()
    with pytest.raises(Exception, match="auth first"):
        lv.get_objectsinlistview()


def test_add_and_delete_objects(monkeypatch):
    lv = ListView()
    lv._apiEndpoints = DummyAPI()
    lv.space_id = "space123"
    lv.list_id = "list123"

    obj = Object()
    obj.id = "obj1"

    lv.add_objectsinlistview([obj])  # Testa adicionar
    lv.delete_objectinlistview(obj)  # Testa deletar

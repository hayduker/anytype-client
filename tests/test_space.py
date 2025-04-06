# test_space.py
import pytest
from anytype.space import Space
from anytype.object import Object
from anytype.type import Type
from anytype.icon import Icon


def test_space_initialization():
    space = Space()
    assert space._apiEndpoints is None
    assert space.name == ""
    assert space.id == ""
    assert space._all_types == []


def test_space_repr():
    space = Space()
    space.name = "MySpace"
    assert repr(space) == "<Space(name=MySpace)>"


def test_get_object_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_object("dummy-id")


def test_delete_object_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.delete_object("dummy-id")


def test_get_objects_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_objects()


def test_get_type_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_type("dummy-id")


def test_get_types_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_types()


def test_get_member_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_member("dummy-id")


def test_get_members_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.get_members()


def test_search_without_auth_raises():
    space = Space()
    with pytest.raises(Exception, match="You need to auth first"):
        space.search("query")


def test_search_without_space_id_raises():
    class DummyApi:
        def search(self, *args, **kwargs):
            return {}

    space = Space()
    space._apiEndpoints = DummyApi()
    space.id = ""
    with pytest.raises(ValueError, match="Space ID is required"):
        space.search("query")


def test_create_object_with_invalid_icon_type_raises():
    space = Space()
    space._apiEndpoints = object()  # dummy value
    space.id = "space-id"

    obj = Object()
    obj.icon = "not-an-icon"
    obj.name = "Test"
    obj.description = "Test Desc"
    obj.body = "Test Body"

    typ = Type()
    typ.template_id = "template-id"
    typ.key = "type-key"

    with pytest.raises(ValueError, match="Invalid icon type"):
        space.create_object(obj, typ)


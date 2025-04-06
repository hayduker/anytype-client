# test_member.py
from anytype import Member


def test_member_initialization():
    m = Member()
    assert m._apiEndpoints is None
    assert m.type == ""
    assert m.id == ""
    assert m.icon == ""
    assert m.name == ""


def test_member_repr():
    m = Member()
    m.name = "Admin"
    assert repr(m) == "<Member(type=Admin)>"

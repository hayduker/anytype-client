# test_object.py
import pytest
from anytype import Object
from anytype import Icon
from unittest.mock import MagicMock


def test_default_object_properties():
    obj = Object()
    assert obj.space_id == ""
    assert obj.id == ""
    assert obj.name == ""
    assert obj.body == ""
    assert obj.description == ""
    assert obj.layout == "basic"
    assert isinstance(obj.blocks, list)
    assert obj.icon == ""


def test_setting_icon_with_emoji():
    obj = Object()
    obj.icon = "📄"
    assert isinstance(obj.icon, Icon)
    assert obj.icon.emoji == "📄"


def test_setting_icon_with_invalid_string_does_nothing():
    obj = Object()
    obj.icon = "not-an-emoji"
    # Should still be string or unchanged
    assert not isinstance(obj.icon, Icon)


def test_repr_output():
    obj = Object()
    obj.name = "Test Object"
    obj.type = {"name": "note"}
    assert repr(obj) == "<Object(name=Test Object,type=note)>"


def test_add_title_and_text_methods():
    obj = Object()
    obj.add_title1("Title 1")
    obj.add_title2("Title 2")
    obj.add_title3("Title 3")
    obj.add_text("This is a paragraph.")
    expected = (
        "# Title 1\n" "## Title 2\n" "### Title 3\n" "This is a paragraph.\n"
    )
    assert obj.body.startswith(expected)


def test_add_codeblock():
    obj = Object()
    obj.add_codeblock("print('Hello')", "python")
    assert "``` python\nprint('Hello')\n```\n" in obj.body


def test_add_bullet_and_checkbox():
    obj = Object()
    obj.add_bullet("Bullet point")
    obj.add_checkbox("Unchecked")
    obj.add_checkbox("Checked", checked=True)
    assert "- Bullet point\n" in obj.body
    assert "- [ ] Unchecked\n" in obj.body
    assert "- [x] Checked\n" in obj.body


def test_add_image():
    obj = Object()
    obj.add_image("http://image.png", "alt", "title")
    assert '![alt](http://image.png "title")\n' in obj.body


def test_export_raises_exception_if_not_authed():
    obj = Object()
    with pytest.raises(Exception, match="You need to auth first"):
        obj.export("/tmp")


def test_export_calls_api_get_export(monkeypatch):
    obj = Object()
    mock_api = MagicMock()
    obj._apiEndpoints = mock_api
    obj.space_id = "space-id"
    obj.id = "object-id"

    obj.export("somefolder", format="markdown")

    mock_api.getExport.assert_called_once_with(
        "space-id", "object-id", "markdown"
    )

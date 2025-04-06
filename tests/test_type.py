# test_type.py
import pytest
from anytype import Type
from anytype import Template
from unittest.mock import MagicMock


def test_default_type_initialization():
    t = Type()
    assert t.name == ""
    assert t.id == ""
    assert t.icon == {}
    assert t.template_id == ""
    assert t._all_templates == []


def test_repr_with_emoji_icon():
    t = Type()
    t.name = "TestType"
    t.icon = {"emoji": "📄"}
    assert repr(t) == "<Type(name=TestType, icon=📄)>"


def test_repr_with_named_icon():
    t = Type()
    t.name = "TestType"
    t.icon = {"name": "icon-name"}
    assert repr(t) == "<Type(name=TestType, icon=icon-name)>"


def test_get_templates_calls_api(monkeypatch):
    t = Type()
    mock_api = MagicMock()
    t._apiEndpoints = mock_api
    t.space_id = "space123"
    t.id = "type123"

    mock_api.getTemplates.return_value = {
        "data": [
            {"id": "tpl1", "name": "Template 1"},
            {"id": "tpl2", "name": "Template 2"},
        ]
    }

    templates = t.get_templates()
    assert len(templates) == 2
    assert all(isinstance(temp, Template) for temp in templates)
    assert templates[0].id == "tpl1"
    assert templates[0].name == "Template 1"


def test_get_templates_without_auth_raises():
    t = Type()
    with pytest.raises(Exception, match="You need to auth first"):
        t.get_templates()


def test_set_template_valid(monkeypatch):
    t = Type()
    mock_tpl1 = Template()
    mock_tpl1.name = "Template 1"
    mock_tpl1.id = "tpl1"
    t._all_templates = [mock_tpl1]

    t.set_template("Template 1")
    assert t.template_id == "tpl1"


def test_set_template_invalid_raises(monkeypatch):
    t = Type()
    mock_tpl = Template()
    mock_tpl.name = "Valid Template"
    mock_tpl.id = "tpl-valid"
    t._all_templates = [mock_tpl]

    with pytest.raises(ValueError, match="does not have a template named"):
        t.set_template("Invalid Template")


def test_get_template(monkeypatch):
    t = Type()
    mock_api = MagicMock()
    t._apiEndpoints = mock_api
    t.space_id = "spaceX"
    t.id = "typeX"

    mock_api.getTemplate.return_value = {
        "data": [{"id": "tpl3", "name": "Template 3"}]
    }

    template = t.get_template("tpl3")
    assert isinstance(template, Template)
    assert template.id == "tpl3"
    assert template.name == "Template 3"


def test_get_template_without_auth_raises():
    t = Type()
    with pytest.raises(Exception, match="You need to auth first"):
        t.get_template("tpl-id")


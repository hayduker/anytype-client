import pytest
import os

from anytype import Anytype, Space, Template, Object, Relation, Block
from pathlib import Path

any = Anytype()
any.auth()


def test_create_space():
    any.create_space("API")
    assert get_apispace()


def get_apispace() -> Space:
    spaces = any.get_spaces()
    for space in spaces:
        if space.name == "API":
            return space
    raise Exception("Space not found")


def test_get_spaces():
    spaces = any.get_spaces()
    assert len(spaces) > 0

    api_space = False
    for space in spaces:
        if space.name == "API":
            api_space = space
            break

    assert api_space

    api_space2 = any.get_space(api_space.id)
    assert api_space2 is not None
    assert api_space2.name == api_space.name


def test_missspaceid():
    space = get_apispace()
    print(space)
    space.id = ""
    with pytest.raises(ValueError):
        space.search("bla bla bla")


def test_template():
    # this is unsued yet, but just to keep testing
    template = Template()
    print(template)


def test_search():
    space = get_apispace()
    values = space.search("Math")
    print(values)


def test_globalsearch():
    query = any.global_search("Isso não deve existir")
    print(query)

    query = any.global_search("Math")
    print(query)


def test_get_types():
    space = get_apispace()
    space._all_types = []

    with pytest.raises(ValueError):
        space.get_type("ExistingType")


def test_relation():
    # this is unsued yet, but just to keep testing
    relation = Relation()
    print(relation)


def test_block():
    # this is unsued yet, but just to keep testing
    block = Block()
    print(block)


def test_spacemethods():
    space = any.get_spaces()[0]
    objects = space.get_objects()
    obj = objects[0]
    obj = space.get_object(obj.id)


def test_templates():
    space = get_apispace()
    objtype = space.get_typebyname("Project")
    print(objtype)

    templates = objtype.get_templates()
    if templates is None:
        raise Exception("No templates found for Project")

    objtype.set_template(templates[0].name)
    objtype._all_templates = []
    objtype.set_template(templates[0].name)
    print(templates[0])

    # template that does not exist
    with pytest.raises(ValueError):
        objtype.set_template("NoExists")


def test_createobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")

    obj = Object()
    obj.name = "Hello World!"
    obj.icon = "🐍"
    obj.body = "`print('Hello World!')`"
    obj.description = "This is an object created from Python Api"

    objtype = space.get_typebyname("Page")
    obj.add_title1("Test!")
    obj.add_title2("Test!")
    obj.add_title3("Test!")
    obj.add_text("normal text")
    obj.add_codeblock("print('Hello World!')")
    obj.add_bullet("Hello World!")
    obj.add_checkbox("Hello World!")
    obj.add_image(
        "https://raw.githubusercontent.com/charlesneimog/"
        + "anytype-client/refs/heads/main/resources/pdf.png"
    )
    obj.add_image(
        "https://raw.githubusercontent.com/charlesneimog/"
        + "anytype-client/refs/heads/main/resources/pdf.png",
        alt="PDF",
        title="PDF",
    )
    created_obj = space.create_object(obj, objtype)
    # Add assertions to verify the object was created
    assert created_obj.name == "Hello World!"
    assert created_obj.icon.emoji == "🐍"
    assert created_obj.description == "This is an object created from Python Api"

    space.search("Hello World")


def test_getmembers():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")
    members = space.get_members()
    assert len(members) > 0


def test_exportobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")
    objs = space.get_objects()
    obj = objs[0]
    assert len(objs) > 0
    obj.export("export")

    # Handle the case for Linux / Flatpak
    if not Path("export").exists() and os.name == "posix":
        pytest.skip("Export test is not supported on flatpak for Linux.")
    else:
        assert Path("export").exists()

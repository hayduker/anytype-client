import pytest
from anytype import Icon


def test_default_icon_properties():
    icon = Icon()
    assert icon.color == "red"
    assert icon.format == "emoji"
    assert icon.emoji == "📄"
    assert icon.file == ""
    assert icon.name == "document"
    assert repr(icon) == "<Icon=📄>"


def test_set_file_sets_format():
    icon = Icon()
    icon.file = "path/to/file"
    assert icon.file == "path/to/file"
    assert icon.format == "file"
    assert repr(icon) == "<Icon(file=File)>"


def test_set_name_sets_format_icon():
    icon = Icon()
    icon.name = "new-icon"
    assert icon.name == "new-icon"
    assert icon.format == "icon"
    assert repr(icon) == "<Icon(AnytypeIcon)>"


def test_set_format_invalid():
    icon = Icon()
    with pytest.raises(ValueError, match="Invalid format"):
        icon.format = "invalid"


def test_set_emoji_when_not_in_emoji_format():
    icon = Icon()
    icon.format = "file"
    with pytest.raises(
        ValueError, match="Emoji can only be set if format is set to emoji"
    ):
        icon.emoji = "😀"


def test_set_emoji_in_emoji_format():
    icon = Icon()
    icon.format = "emoji"
    icon.emoji = "😀"
    assert icon.emoji == "😀"


def test_update_with_json_emoji():
    icon = Icon()
    icon._update_with_json({"format": "emoji", "format": "emoji"})
    assert icon.format == "emoji"


def test_update_with_json_icon():
    icon = Icon()
    icon._update_with_json({"format": "icon", "icon": "icon-name"})
    assert icon.format == "icon"


def test_update_with_json_file():
    icon = Icon()
    icon._update_with_json({"format": "file", "file": "somefile.txt"})
    assert icon.format == "file"
    assert icon.file == "somefile.txt"


def test_update_with_json_invalid_format():
    icon = Icon()
    with pytest.raises(ValueError, match="Invalid format"):
        icon._update_with_json({"format": "unknown"})


def test_get_json_emoji():
    icon = Icon()
    icon.format = "emoji"
    icon.emoji = "🌟"
    assert icon._get_json() == {"emoji": "🌟", "format": "emoji"}


def test_get_json_icon():
    icon = Icon()
    icon.name = "icon-name"
    icon.color = "blue"
    icon.format = "icon"
    icon._get_json() == {"color": "blue", "format": "icon", "name": "icon-name"}


def test_get_json_file():
    icon = Icon()
    icon.file = "somefile.txt"
    assert icon._get_json() == {"file": "somefile.txt", "format": "file"}

from pathlib import Path
import platform
import re

from .block import Block
from .type import Type
from .icon import Icon
from .api import apiEndpoints


class Object:
    def __init__(self):
        self._apiEndpoints: apiEndpoints | None = None
        self.id: str = ""
        self.source: str = ""
        self.type: dict = {}
        self.name: str = ""
        self._icon: str | Icon = ""
        self.body: str = ""
        self.description: str = ""
        self.blocks: list[Block] = []
        self.details = []
        self.layout: str = "basic"
        self.properties: list = []

        self.root_id: str = ""
        self.space_id: str = ""
        self.template_id: str = ""

        self.snippet: str = ""
        self.type_key: str = ""

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )

        if bool(emoji_pattern.fullmatch(value)):
            icon = Icon()
            icon.emoji = value
            self._icon = icon

    def export(self, folder: str, format: str = "markdown") -> None:
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")

        path = Path(folder)
        if not path.is_absolute():
            path = Path.cwd() / path

        assert format in ["markdown", "protobuf"]
        self._apiEndpoints.getExport(self.space_id, self.id, format)
        if platform.system() == "Linux":
            print("Note that this will not work on Anytype for flatpak, even without any errors")

    def add_type(self, type: Type):
        self.template_id = type.template_id
        self.type_key = type.key

    # ╭──────────────────────────────────────╮
    # │ Hope that Anytype API make some way  │
    # │ to create blocks, then this will be  │
    # │           probably removed           │
    # ╰──────────────────────────────────────╯
    def add_title1(self, text) -> None:
        self.body += f"# {text}\n"

    def add_title2(self, text) -> None:
        self.body += f"## {text}\n"

    def add_title3(self, text) -> None:
        self.body += f"### {text}\n"

    def add_text(self, text) -> None:
        self.body += f"{text}\n"

    def add_codeblock(self, code, language=""):
        self.body += f"``` {language}\n{code}\n```\n"

    def add_bullet(self, text) -> None:
        self.body += f"- {text}\n"

    def add_checkbox(self, text, checked=False) -> None:
        self.body += f"- [x] {text}\n" if checked else f"- [ ] {text}\n"

    def add_image(self, image_url: str, alt: str = "", title: str = "") -> None:
        if title:
            self.body += f'![{alt}]({image_url} "{title}")\n'
        else:
            self.body += f"![{alt}]({image_url})\n"

    def __repr__(self):
        return f"<Object(name={self.name},type={self.type['name']})>"

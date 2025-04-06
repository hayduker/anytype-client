import requests
from pathlib import Path
import platform

from .config import END_POINTS
from .block import Block
from .error import ResponseHasError


class Object:
    def __init__(self):
        self._headers: dict = {}
        self.space_id: str = ""
        self.id: str = ""
        self.source: str = ""
        self.type: str = "Page"
        self.name: str = ""
        self.icon: str = ""
        self.body: str = ""
        self.description: str = ""
        self.blocks: list[Block] = []
        self.details = []
        self.layout: str = "basic"
        self.root_id: str = ""
        self.snippet: str = ""
        self.space_id: str = ""

    def export(self, folder: str, format: str = "markdown") -> None:
        path = Path(folder)
        if not path.is_absolute():
            path = Path.cwd() / path

        assert format in ["markdown", "protobuf"]
        url = END_POINTS["getExport"].format(self.space_id, self.id, format)
        payload = {"path": str(path)}
        response = requests.get(url, headers=self._headers, json=payload)
        ResponseHasError(response)
        if platform.system() == "Linux":
            print("Note that this will not work on Anytype for flatpak")

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
        return f"<Object(name={self.name},type_id={self.type})>"

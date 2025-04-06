class Icon:
    def __init__(self):
        self.color: str = "red"
        self._emoji: str = "📄"
        self._file: str = ""
        self._format = "emoji"
        self._name = "document"

    def _update_with_json(self, json: dict) -> None:
        if json["format"] == "emoji":
            self.emoji = json["format"]
            self.format = "emoji"
        elif json["format"] == "icon":
            self.icon = json["icon"]
            self.format = "icon"
        elif json["format"] == "file":
            self.file = json["file"]
            self.format = "file"
        else:
            raise ValueError("Invalid format")

    def _get_json(self) -> dict:
        if self.format == "emoji":
            return {
                "emoji": self.emoji,
                "format": self.format,
            }
        elif self.format == "icon":
            return {
                "color": self.color,
                "format": self.format,
                "name": self.name,
            }
        elif self.format == "file":
            return {
                "file": self.file,
                "format": self.format,
            }
        else:
            raise ValueError("Invalid format")

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, value) -> None:
        self._file = value
        self._format = "file"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value
        self._format = "icon"

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, value) -> None:
        if value not in ["emoji", "file", "icon"]:
            raise ValueError("Invalid format")
        self._format = value

    @property
    def emoji(self) -> str:
        return self._emoji

    @emoji.setter
    def emoji(self, value) -> None:
        if self.format != "emoji":
            raise ValueError("Emoji can only be set if format is set to emoji")
        self._emoji = value

    def __repr__(self) -> str:
        if self.format == "emoji":
            return f"<Icon={self.emoji}>"
        elif self.format == "icon":
            return "<Icon(AnytypeIcon)>"
        elif self.format == "file":
            return "<Icon(file=File)>"
        else:
            raise ValueError("Invalid format")

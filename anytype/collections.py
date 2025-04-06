from copy import deepcopy

from .icon import Icon


class Collections:
    def __init__(self):
        self.name = ""

    def __repr__(self):
        return f"<Collections(name={self.name})>"

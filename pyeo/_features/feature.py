from typing import Protocol


class Feature(Protocol):

    def analyze(self, ctx) -> bool: ...

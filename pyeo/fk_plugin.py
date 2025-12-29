# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

# flake8: noqa: WPS232

import ast
from collections.abc import Generator
from typing import final

from pyeo.visitor_protocol import VisitorWithProblems


@final
class FkPlugin:
    """Fake flake8 plugin."""

    def __init__(self, tree: ast.AST, visitors: list[VisitorWithProblems]) -> None:
        """Ctor."""
        self._tree = tree
        self._visitors = visitors

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        for visitor in self._visitors:
            visitor.visit(self._tree)
            for line in visitor.problems:  # noqa: WPS526
                yield (line[0], line[1], line[2], type(self))

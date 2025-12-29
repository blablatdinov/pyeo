# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""Protocol for visitors with problems attribute."""

import ast
from typing import Protocol


class VisitorWithProblems(Protocol):
    """Protocol for visitors with problems attribute."""

    problems: list[tuple[int, int, str]]

    def visit(self, node: ast.AST) -> None:
        """Visit AST node."""

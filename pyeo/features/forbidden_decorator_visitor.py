# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""ForbiddenDecoratorVisitor."""

import argparse
import ast
from typing import final


@final
class ForbiddenDecoratorVisitor(ast.NodeVisitor):
    """ForbiddenDecoratorVisitor."""

    def __init__(self, options: argparse.Namespace) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by methods.

        :param node: ast.ClassDef
        """
        for deco in node.decorator_list:
            if isinstance(deco, ast.Name) and deco.id == 'staticmethod':
                self.problems.append((node.lineno, node.col_offset, 'PEO400 Staticmethod is forbidden'))
        self.generic_visit(node)

# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""NoPropertyDecoratorVisitor."""

import argparse
import ast
from typing import final


@final
class NoPropertyDecoratorVisitor(ast.NodeVisitor):
    """Visitor that forbids the use of @property decorator."""

    def __init__(self, options: argparse.Namespace) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Visit function definitions to check for @property decorator.

        :param node: ast.FunctionDef
        """
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                self.problems.append((
                    node.lineno,
                    node.col_offset,
                    'PEO500 @property decorator is forbidden',
                ))
        self.generic_visit(node)

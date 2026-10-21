# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""NoReflectionVisitor."""

import argparse
import ast
from typing import final


@final
class NoReflectionVisitor(ast.NodeVisitor):
    """NoReflectionVisitor."""

    def __init__(self, options: argparse.Namespace) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []
        self._forbidden = frozenset((
            'isinstance',
            'issubclass',
            'hasattr',
            'getattr',
            'setattr',
            'delattr',
            'cast',
        ))

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        """Visit by calls.

        :param node: ast.Call
        """
        name = self._name(node)
        if name:
            self.problems.append((node.lineno, node.col_offset, 'PEO700 reflection is forbidden: {0}'.format(name)))
        self.generic_visit(node)

    def visit_MatchClass(self, node: ast.MatchClass) -> None:  # noqa: N802
        """Visit by class patterns of match statements.

        :param node: ast.MatchClass
        """
        self.problems.append(
            (node.lineno, node.col_offset, 'PEO700 reflection is forbidden: {0}'.format(ast.unparse(node.cls))),
        )
        self.generic_visit(node)

    def _name(self, node: ast.Call) -> str:
        func = node.func
        if isinstance(func, ast.Name) and func.id in self._forbidden:
            return func.id
        if isinstance(func, ast.Name) and func.id == 'type' and len(node.args) == 1 and not node.keywords:
            return func.id
        if isinstance(func, ast.Attribute) and func.attr == 'cast' and isinstance(func.value, ast.Name):
            return func.attr if func.value.id == 'typing' else ''
        return ''

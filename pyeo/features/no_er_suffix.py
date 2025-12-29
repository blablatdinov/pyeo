# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""NoErSuffix."""

import argparse
import ast
from typing import final


@final
class NoErSuffix(ast.NodeVisitor):
    """NoErSuffix."""

    def __init__(self, options: argparse.Namespace) -> None:
        """Ctor."""
        self._options = options
        self.problems: list[tuple[int, int, str]] = []
        self._whitelist = {
            'User',
            'Identifier',
        } | set(self._options.available_er_names)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        class_name = node.name
        if class_name.endswith('er'):
            for whitelist_suffix in self._whitelist:
                if class_name.endswith(whitelist_suffix):
                    break
            else:
                self.problems.append((node.lineno, node.col_offset, 'PEO300 "er" suffix forbidden'))
        self.generic_visit(node)

# The MIT License (MIT).
#
# Copyright (c) 2023-2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

"""CodeFreeCtorVisitor."""

import ast
from typing import final


@final
class CodeFreeCtorVisitor(ast.NodeVisitor):
    """CodeFreeCtorVisitor."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        for elem in node.body:
            if not isinstance(elem, ast.FunctionDef) and not isinstance(elem, ast.AsyncFunctionDef):
                continue
            if elem.name == '__init__':
                for body_elem in elem.body:
                    self._iter_ctor_ast(body_elem)
        self.generic_visit(node)

    def _iter_ctor_ast(self, node):
        if not isinstance(node, (ast.Return, ast.Assign)):
            self.problems.append((node.lineno, node.col_offset, 'PEO100 Ctor contain code'))

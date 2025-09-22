# The MIT License (MIT).
#
# Copyright (c) 2023-2025 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
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

"""NoGetterMethodsVisitor."""

import ast
from typing import final


@final
class NoGetterMethodsVisitor(ast.NodeVisitor):
    """Visitor that forbids methods that return object attributes (getter methods)."""

    def __init__(self, options) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Visit function definitions to check for getter methods.

        :param node: ast.FunctionDef
        """
        # Skip if function is not a method (no self parameter)
        if not self._is_method(node):
            self.generic_visit(node)
            return

        # Check if method name starts with "get" or "get_"
        if self._is_getter_by_name(node.name):
            self.problems.append((
                node.lineno,
                node.col_offset,
                f'PEO601 Method "{node.name}" starts with "get" and should be avoided',
            ))
        # Only check for simple getters if method name doesn't start with "get"
        elif len(node.args.args) == 1 and self._is_simple_getter(node):
            self.problems.append((
                node.lineno,
                node.col_offset,
                f'PEO602 Method "{node.name}" is a getter and should be avoided',
            ))

        self.generic_visit(node)

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (has self parameter).

        :param node: ast.FunctionDef
        :return: True if function is a method
        """
        return (
            node.args.args and
            isinstance(node.args.args[0], ast.arg) and
            node.args.args[0].arg == 'self'
        )

    def _is_getter_by_name(self, method_name: str) -> bool:
        """Check if method name starts with 'get'.

        :param method_name: Name of the method
        :return: True if method name starts with 'get'
        """
        return method_name.startswith('get')

    def _is_simple_getter(self, node: ast.FunctionDef) -> bool:
        """Check if method is a simple getter (only returns self.attribute).

        :param node: ast.FunctionDef
        :return: True if method is a simple getter
        """
        if not node.body or len(node.body) != 1:
            return False

        stmt = node.body[0]

        # Check for simple return statement
        if isinstance(stmt, ast.Return):
            return self._is_attribute_access(stmt.value)

        # Check for return statement in if/else blocks
        if isinstance(stmt, ast.If):
            return (
                self._has_simple_return(stmt.body) and
                (not stmt.orelse or self._has_simple_return(stmt.orelse))
            )

        return False

    def _is_attribute_access(self, node: ast.AST | None) -> bool:
        """Check if node is a simple attribute access (self.attribute).

        :param node: ast.AST
        :return: True if node is attribute access
        """
        if not isinstance(node, ast.Attribute):
            return False

        # Check if it's self.attribute
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            return True

        # Check for chained attribute access like self.obj.attr
        if isinstance(node.value, ast.Attribute):
            return self._is_attribute_access(node.value)

        return False

    def _has_simple_return(self, stmts: list[ast.stmt]) -> bool:
        """Check if list of statements contains only simple return.

        :param stmts: List of statements
        :return: True if only simple return statements
        """
        if len(stmts) != 1:
            return False

        stmt = stmts[0]
        if isinstance(stmt, ast.Return):
            return self._is_attribute_access(stmt.value)

        return False

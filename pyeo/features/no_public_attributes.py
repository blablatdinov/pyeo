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

"""NoPublicAttributesVisitor."""

import ast
from typing import final

from pyeo.utils.class_is_protocol import class_is_enum, class_is_exception, class_is_typeddict


@final
class NoPublicAttributesVisitor(ast.NodeVisitor):
    """NoPublicAttributesVisitor."""

    def __init__(self, options) -> None:
        """Ctor."""
        self._options = options
        self.problems: list[tuple[int, int, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231
        """Visit by classes.

        :param node: ast.ClassDef
        """
        if self._should_skip_class(node):
            self.generic_visit(node)
            return
        for elem in node.body:
            if isinstance(elem, ast.Assign):
                self._check_assign_attributes(elem)
            elif isinstance(elem, ast.AnnAssign):
                self._check_ann_assign_attributes(elem)
        self.generic_visit(node)

    def _should_skip_class(self, node: ast.ClassDef) -> bool:
        """Check if class should be skipped from public attributes check.

        :param node: ast.ClassDef
        :return: True if class should be skipped
        """
        return any([
            class_is_enum(node),
            class_is_exception(node),
            class_is_typeddict(node),
        ])

    def _check_assign_attributes(self, node: ast.Assign) -> None:
        """Check assign attributes for public names.

        :param node: ast.Assign
        """
        for target in node.targets:
            if isinstance(target, ast.Name):
                if not target.id.startswith('_'):
                    self.problems.append((
                        node.lineno,
                        node.col_offset,
                        f'PEO300 class attribute "{target.id}" should be private',
                    ))

    def _check_ann_assign_attributes(self, node: ast.AnnAssign) -> None:
        """Check annotated assign attributes for public names.

        :param node: ast.AnnAssign
        """
        if isinstance(node.target, ast.Name):
            if not node.target.id.startswith('_'):
                self.problems.append((
                    node.lineno,
                    node.col_offset,
                    f'PEO300 class attribute "{node.target.id}" should be private',
                ))

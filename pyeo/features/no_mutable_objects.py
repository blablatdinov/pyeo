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

"""NoMutableObjectsVisitor."""

import ast
from typing import final

from pyeo.utils.class_is_protocol import class_is_not_obj_factory


@final
class NoMutableObjectsVisitor(ast.NodeVisitor):
    """NoMutableObjectsVisitor."""

    def __init__(self, options) -> None:
        """Ctor."""
        self._options = options
        self.problems: list[tuple[int, int, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        frozen_found = False
        if class_is_not_obj_factory(node):
            self.generic_visit(node)
            return
        for deco in node.decorator_list:
            if isinstance(deco, ast.Name) and deco.id == 'frozen':
                frozen_found = True
                break
            elif isinstance(deco, ast.Attribute) and deco.attr == 'frozen' and deco.value.id == 'attrs':
                frozen_found = True
                break
            elif isinstance(deco, ast.Call):
                if isinstance(deco.func, ast.Attribute) and hasattr(deco.func, 'id') and deco.func.id == 'define':
                    for keyword in deco.keywords:
                        if keyword.arg == 'frozen' and keyword.value.value:
                            frozen_found = True
                            break
                elif isinstance(deco.func, ast.Attribute) and deco.func.attr == 'define':
                    frozen_found = self._frozen(deco.keywords)
                elif isinstance(deco.func, ast.Name) and deco.func.id == 'define':
                    frozen_found = self._frozen(deco.keywords)
                elif isinstance(deco.func, ast.Name) and deco.func.id == 'frozen':
                    frozen_found = True
                    break
                elif isinstance(deco.func, ast.Attribute) and deco.func.attr == 'dataclass':
                    frozen_found = self._frozen(deco.keywords)
                elif isinstance(deco.func, ast.Name) and deco.func.id == 'dataclass':
                    frozen_found = self._frozen(deco.keywords)
                elif deco.func.value.id == 'attrs' and deco.func.attr == 'frozen':
                    frozen_found = True
                    break
        if not frozen_found:
            self.problems.append((node.lineno, node.col_offset, 'PEO200 class must be frozen'))
        self.generic_visit(node)

    def _frozen(self, keywords: list[ast.keyword]) -> bool:
        for keyword in keywords:
            if keyword.arg == 'frozen' and keyword.value.value:
                return True
        return False

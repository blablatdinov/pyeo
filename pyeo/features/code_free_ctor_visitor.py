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

"""AssignmentOnlyCtorVisitor."""

import ast
from typing import final


@final
class CodeFreeCtorVisitor(ast.NodeVisitor):
    """CodeFreeCtorVisitor."""

    def __init__(self, options) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        for elem in node.body:
            if not isinstance(elem, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if elem.name == '__init__':
                self._check_constructor_body(elem, 'PEO101 __init__ method should contain only assignments')
            elif self._is_classmethod(elem):
                self._check_constructor_body(elem, 'PEO102 @classmethod should contain only cls() call')
        self.generic_visit(node)
    def _is_classmethod(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Проверяет, является ли метод classmethod."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'classmethod':
                return True
            elif isinstance(decorator, ast.Attribute) and decorator.attr == 'classmethod':
                return True
        return False

    def _check_constructor_body(self, node: ast.FunctionDef | ast.AsyncFunctionDef, error_message: str) -> None:
        """Проверяет тело конструктора на наличие только операций присваивания."""
        for body_elem in node.body:
            if isinstance(body_elem, (ast.Assign, ast.AnnAssign)):
                if node.name == '__init__' and not self._is_valid_assignment(body_elem, node):
                    self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))
                continue
            elif isinstance(body_elem, ast.Return):
                if body_elem.value is None:
                    if node.name == '__init__':
                        continue
                    else:
                        self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))
                else:
                    if self._is_classmethod(node) and isinstance(body_elem.value, ast.Call) and self._is_valid_cls_call(body_elem.value, node):
                        continue
                    else:
                        self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))
            elif isinstance(body_elem, ast.Expr) and isinstance(body_elem.value, ast.Constant) and isinstance(body_elem.value.value, str):
                continue
            else:
                self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))

    def _is_valid_cls_call(self, node: ast.Call, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Проверяет, является ли вызов cls() валидным (все аргументы - константы или аргументы функции)."""
        if not isinstance(node.func, ast.Name) or node.func.id != 'cls':
            return False
        arg_names = {arg.arg for arg in func_node.args.args}
        for arg in node.args:
            if isinstance(arg, ast.Name) and arg.id in arg_names:
                continue
            elif isinstance(arg, ast.Constant):
                continue
            else:
                return False
        return True

    def _is_valid_assignment(self, node: ast.Assign | ast.AnnAssign, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Проверяет, является ли присваивание валидным (использует аргументы функции или константы)."""
        arg_names = {arg.arg for arg in func_node.args.args}
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    if isinstance(node.value, ast.Name) and node.value.id in arg_names:
                        return True
                    elif isinstance(node.value, ast.Constant):
                        return True
            return False
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id in arg_names:
                    return True
                elif isinstance(node.value, ast.Constant):
                    return True
            return False
        return False

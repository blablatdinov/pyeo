# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""AssignmentOnlyCtorVisitor."""

import argparse
import ast
from typing import final


@final
class CodeFreeCtorVisitor(ast.NodeVisitor):
    """CodeFreeCtorVisitor."""

    def __init__(self, options: argparse.Namespace) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        if self._is_enum_class(node):
            self.generic_visit(node)
            return
        for elem in node.body:
            if not isinstance(elem, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if elem.name == '__init__':
                self._check_constructor_body(elem, 'PEO101 __init__ method should contain only assignments')
            elif self._is_classmethod(elem):
                self._check_constructor_body(elem, 'PEO102 @classmethod should contain only cls() call')
        self.generic_visit(node)

    def _is_enum_class(self, node: ast.ClassDef) -> bool:
        for base in node.bases:
            if (
                (isinstance(base, ast.Name) and base.id.endswith('Enum'))
                or (isinstance(base, ast.Attribute) and base.attr.endswith('Enum'))
            ):
                return True
        return False

    def _is_classmethod(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        for decorator in node.decorator_list:
            if (
                (isinstance(decorator, ast.Name) and decorator.id == 'classmethod')
                or (isinstance(decorator, ast.Attribute) and decorator.attr == 'classmethod')
            ):
                return True
        return False

    def _check_constructor_body(self, node: ast.FunctionDef | ast.AsyncFunctionDef, error_message: str) -> None:
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
                    if self._is_classmethod(node) and isinstance(body_elem.value, ast.Call):
                        if self._is_valid_cls_call(body_elem.value, node) or self._is_constructor_call(body_elem.value):
                            continue
                        else:
                            self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))
                    else:
                        self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))
            elif (
                isinstance(body_elem, ast.Expr)
                and isinstance(body_elem.value, ast.Constant)
                and isinstance(body_elem.value.value, str)
            ):
                continue
            else:
                self.problems.append((body_elem.lineno, body_elem.col_offset, error_message))

    def _is_valid_cls_call(self, node: ast.Call, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        if not isinstance(node.func, ast.Name) or node.func.id != 'cls':
            return False
        arg_names = {arg.arg for arg in func_node.args.args}
        if func_node.args.vararg:
            arg_names.add(func_node.args.vararg.arg)
        if func_node.args.kwarg:
            arg_names.add(func_node.args.kwarg.arg)
        if func_node.args.kwonlyargs:
            for kwarg in func_node.args.kwonlyargs:
                arg_names.add(kwarg.arg)
        for arg in node.args:
            if isinstance(arg, ast.Name) and arg.id in arg_names:
                continue
            elif isinstance(arg, ast.Constant):
                continue
            elif isinstance(arg, ast.Call):
                if self._is_constructor_call(arg):
                    continue
                else:
                    return False
            else:
                return False
        return True

    def _is_constructor_call(self, node: ast.Call) -> bool:
        if isinstance(node.func, ast.Name):
            return node.func.id[0].isupper() if node.func.id else False
        elif isinstance(node.func, ast.Attribute):
            return self._is_class_reference(node.func.value)
        return False

    def _is_class_reference(self, node: ast.expr) -> bool:
        if isinstance(node, ast.Name):
            return node.id[0].isupper() if node.id else False
        elif isinstance(node, ast.Attribute):
            return self._is_class_reference(node.value)
        return False

    def _is_valid_assignment(
        self,
        node: ast.Assign | ast.AnnAssign,
        func_node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> bool:
        arg_names = {arg.arg for arg in func_node.args.args}
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    (
                        isinstance(target, ast.Attribute)
                        and (isinstance(node.value, ast.Name) and node.value.id in arg_names)
                    )
                    or isinstance(node.value, ast.Constant)
                ):
                    return True
            return False
        elif isinstance(node, ast.AnnAssign):
            return (
                (
                    isinstance(node.target, ast.Attribute)
                    and (isinstance(node.value, ast.Name) and node.value.id in arg_names)
                )
                or isinstance(node.value, ast.Constant)
            )
        return False

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

import ast


def class_is_protocol(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and base.value.id == 'Protocol':
                return True
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and base.value.id != 'Protocol':
                continue
        if isinstance(base, ast.Name) and base.id != 'Protocol':
            continue
        if isinstance(base, ast.Name) and base.id == 'Protocol':
            return True
        if base.attr == 'Protocol':
            return True
    return False


def class_is_typeddict(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and base.value.id == 'TypedDict':
                return True
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and base.value.id != 'TypedDict':
                continue
        if isinstance(base, ast.Name) and base.id != 'TypedDict':
            continue
        if isinstance(base, ast.Name) and base.id == 'TypedDict':
            return True
        if base.attr == 'TypedDict':
            return True
    return False


def class_is_enum(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and base.value.id.endswith('Enum'):
                return True
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and not base.value.id.endswith('Enum'):
                continue
        if isinstance(base, ast.Name) and not base.id.endswith('Enum'):
            continue
        if isinstance(base, ast.Name) and base.id.endswith('Enum'):
            return True
        if base.attr.endswith('Enum'):
            return True
    return False


def class_is_exception(node: ast.ClassDef) -> bool:
    exception_name = lambda name: name.endswith('Exception') or name.endswith('Error')
    for base in node.bases:
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and exception_name(base.value.id):
                return True
        if isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name) and not exception_name(base.value.id):
                continue
        if isinstance(base, ast.Name) and not exception_name(base.id):
            continue
        if isinstance(base, ast.Name) and exception_name(base.id):
            return True
        if exception_name(base.attr):
            return True
    return False


def class_is_not_obj_factory(node: ast.ClassDef) -> bool:
    return any([
        class_is_protocol(node),
        class_is_enum(node),
        class_is_exception(node),
        class_is_typeddict(node),
    ])

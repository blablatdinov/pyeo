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
    """Check if a class is a Protocol."""
    for base in node.bases:
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and base.value.id == 'Protocol'
        ):
            return True
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and base.value.id != 'Protocol'
        ):
            continue
        if isinstance(base, ast.Name) and base.id != 'Protocol':
            continue
        if isinstance(base, ast.Name) and base.id == 'Protocol':
            return True
        if isinstance(base, ast.Attribute) and base.attr == 'Protocol':
            return True
    return False


def class_is_typeddict(node: ast.ClassDef) -> bool:
    """Check if a class is a TypedDict."""
    for base in node.bases:
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and base.value.id == 'TypedDict'
        ):
            return True
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and base.value.id != 'TypedDict'
        ):
            continue
        if isinstance(base, ast.Name) and base.id != 'TypedDict':
            continue
        if isinstance(base, ast.Name) and base.id == 'TypedDict':
            return True
        if isinstance(base, ast.Attribute) and base.attr == 'TypedDict':
            return True
    return False


def class_is_enum(node: ast.ClassDef) -> bool:
    """Check if a class is an Enum."""
    for base in node.bases:
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and base.value.id.endswith('Enum')
        ):
            return True
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and not base.value.id.endswith('Enum')
        ):
            continue
        if isinstance(base, ast.Name) and not base.id.endswith('Enum'):
            continue
        if isinstance(base, ast.Name) and base.id.endswith('Enum'):
            return True
        if isinstance(base, ast.Attribute) and base.attr.endswith('Enum'):
            return True
    return False


def class_is_exception(node: ast.ClassDef) -> bool:
    """Check if a class is an Exception."""
    for base in node.bases:
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and _is_exception_check_name(base.value.id)
        ):
            return True
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and not _is_exception_check_name(base.value.id)
        ):
            continue
        if isinstance(base, ast.Name) and not _is_exception_check_name(base.id):
            continue
        if isinstance(base, ast.Name) and _is_exception_check_name(base.id):
            return True
        if isinstance(base, ast.Attribute) and _is_exception_check_name(base.attr):
            return True
    return False


def _is_exception_check_name(name: str) -> bool:
    return name.endswith(('Exception', 'Error'))


def class_is_not_obj_factory(node: ast.ClassDef) -> bool:
    """Check if a class is not an object factory (Protocol, Enum, Exception, or TypedDict)."""
    return any([
        class_is_protocol(node),
        class_is_enum(node),
        class_is_exception(node),
        class_is_typeddict(node),
    ])

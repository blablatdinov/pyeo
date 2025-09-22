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

"""Tests for NoPropertyDecoratorVisitor."""

import argparse
import ast

from pyeo.features.no_property_decorator import NoPropertyDecoratorVisitor


def test_no_property_decorator_allowed() -> None:
    """Test that functions without @property decorator are allowed."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_vaiue(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoPropertyDecoratorVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 0


def test_property_decorator_forbidden() -> None:
    """Test that @property decorator is forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   @property',
        '   def get_vaiue(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoPropertyDecoratorVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO500 @property decorator is forbidden'


def test_multiple_property_decorators() -> None:
    """Test that multiple @property decorators are detected."""
    code = '\n'.join([
        'class MyClass:',
        '   @property',
        '   def value1(self):',
        '       return self._value1',
        '   @property',
        '   def value2(self):',
        '       return self._value2',
    ])

    tree = ast.parse(code)
    visitor = NoPropertyDecoratorVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 2
    assert all(problem[2] == 'PEO500 @property decorator is forbidden' for problem in visitor.problems)


def test_other_decorators_allowed() -> None:
    """Test that other decorators are allowed."""
    code = '\n'.join([
        'class MyClass:',
        '   @staticmethod',
        '   def value1(self):',
        '       return self._value1',
        '   @classmethod',
        '   def value2(self):',
        '       return self._value2',
    ])

    tree = ast.parse(code)
    visitor = NoPropertyDecoratorVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 0


def test_property_with_other_decorators() -> None:
    """Test that @property with other decorators is still forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   @property',
        '   @staticmethod',
        '   def value1(self):',
        '       return self._value1',
    ])

    tree = ast.parse(code)
    visitor = NoPropertyDecoratorVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO500 @property decorator is forbidden'

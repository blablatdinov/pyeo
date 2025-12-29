# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

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

# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""Tests for NoGetterMethodsVisitor."""

import argparse
import ast

from pyeo.features.no_getter_methods import NoGetterMethodsVisitor


def test_simple_getter_forbidden() -> None:
    """Test that simple getter methods are forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_chained_attribute_getter_forbidden() -> None:
    """Test that getters with chained attributes are forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_nested_value(self):',
        '       return self.obj.attr',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_nested_value" starts with "get" and should be avoided'


def test_getter_with_conditional_forbidden_by_name() -> None:
    """Test that methods starting with 'get' are forbidden even with conditional logic."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self):',
        '       if self._value is None:',
        '           return "default"',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_method_with_parameters_forbidden_by_name() -> None:
    """Test that methods starting with 'get' are forbidden even with parameters."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self, key):',
        '       return self._value[key]',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_non_method_function_allowed() -> None:
    """Test that non-method functions are allowed."""
    code = '\n'.join([
        'def get_value():',
        '    return "value"',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 0


def test_method_with_complex_logic_forbidden_by_name() -> None:
    """Test that methods starting with 'get' are forbidden even with complex logic."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self, key):',
        '       result = self._value',
        '       if result:',
        '           result = result.upper()',
        '       return result',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_method_returning_none_forbidden_by_name() -> None:
    """Test that methods starting with 'get' are forbidden even when returning None."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self):',
        '       return None',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_method_returning_literal_forbidden_by_name() -> None:
    """Test that methods starting with 'get' are forbidden even when returning literals."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value(self):',
        '       return "constant"',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get_value" starts with "get" and should be avoided'


def test_multiple_getters_detected() -> None:
    """Test that multiple getters are detected."""
    code = '\n'.join([
        'class MyClass:',
        '   def get_value1(self):',
        '       return self._value1',
        '   def get_value2(self):',
        '       return self._value2',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 2
    assert visitor.problems[0][2] == 'PEO601 Method "get_value1" starts with "get" and should be avoided'
    assert visitor.problems[1][2] == 'PEO601 Method "get_value2" starts with "get" and should be avoided'


def test_get_method_forbidden() -> None:
    """Test that method named 'get' is forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def get(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "get" starts with "get" and should be avoided'


def test_getter_method_forbidden() -> None:
    """Test that method starting with 'get_' is forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def getter(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "getter" starts with "get" and should be avoided'


def test_getting_method_forbidden() -> None:
    """Test that method starting with 'get' is forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def getting(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO601 Method "getting" starts with "get" and should be avoided'


def test_methods_not_starting_with_get_but_simple_getters_forbidden() -> None:
    """Test that methods not starting with 'get' but are simple getters are forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def value(self):',
        '       return self._value',
        '   def retrieve(self):',
        '       return self._value',
        '   def fetch(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 3
    assert visitor.problems[0][2] == 'PEO602 Method "value" is a getter and should be avoided'
    assert visitor.problems[1][2] == 'PEO602 Method "retrieve" is a getter and should be avoided'
    assert visitor.problems[2][2] == 'PEO602 Method "fetch" is a getter and should be avoided'


def test_methods_with_complex_logic_allowed() -> None:
    """Test that methods with complex logic are allowed."""
    code = '\n'.join([
        'class MyClass:',
        '   def value(self):',
        '       if self._value is None:',
        '           return "default"',
        '       return self._value',
        '   def retrieve(self, key):',
        '       return self._values[key]',
        '   def fetch(self):',
        '       result = self._value',
        '       if result:',
        '           result = result.upper()',
        '       return result',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 0


def test_simple_getter_by_behavior_forbidden() -> None:
    """Test that methods that are simple getters by behavior are forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def value(self):',
        '       return self._value',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO602 Method "value" is a getter and should be avoided'


def test_simple_getter_with_chained_attributes_forbidden() -> None:
    """Test that methods returning chained attributes are forbidden."""
    code = '\n'.join([
        'class MyClass:',
        '   def nested_value(self):',
        '       return self.obj.attr',
    ])

    tree = ast.parse(code)
    visitor = NoGetterMethodsVisitor(argparse.Namespace())
    visitor.visit(tree)
    assert len(visitor.problems) == 1
    assert visitor.problems[0][2] == 'PEO602 Method "nested_value" is a getter and should be avoided'

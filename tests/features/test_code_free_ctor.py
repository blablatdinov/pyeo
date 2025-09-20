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

import pytest
from pyeo.features.code_free_ctor_visitor import CodeFreeCtorVisitor


def test(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        return cls(cost)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_ctor_docstring(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '    def __init__(self, cost):',
            '        """Ctor."""',
            '        self._cost = cost',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        """Ctor."""',
            '        return cls(cost)',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_return_decorated(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        """Ctor."""',
            '        return Residential(cls(cost))',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_iterable_param(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '    @classmethod',
            '    def secondary_ctor(cls, cost, *places):',
            '        """Ctor."""',
            '        return cls(cost, places)',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_param_after_args(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '    @classmethod',
            '    def secondary_ctor(cls, cost, *places, debug_mode):',
            '        """Ctor."""',
            '        return cls(cost, places, debug_mode)',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_ctor_typehint(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost: int | None = None',
            '',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        return cls(cost)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_ctor_object_composition(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost: int | None = None',
            '',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        return cls(PositiveInt(cost))',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_call_function(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost: int | None = None',
            '',
            '    @classmethod',
            '    def secondary_ctor(cls, cost):',
            '        return cls(validate(cost))',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert got


def test_init_with_only_assignments(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_init_with_ann_assign(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost: int = cost',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_valid_classmethod(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def create(cls, cost):',
            '        return cls(cost)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_init_with_return_without_value(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '        return',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


@pytest.mark.parametrize('ctor_body', [
    '\n'.join([
        '        self._cost = cost',
        '        if cost < 0:',
        '            self._cost = 0',
    ]),
    '\n'.join([
        '        self._cost = [0]',
    ]),
    '\n'.join([
        '        print("Creating house")',
    ]),
])
def test_invalid_init(plugin_run, options_factory, ctor_body):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            ctor_body,
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    # Проверяем, что есть ошибка с правильным сообщением, независимо от номера строки
    assert len(got) == 1
    assert got[0][2] == 'PEO101 __init__ method should contain only assignments'


@pytest.mark.parametrize('ctor_body', [
    '\n'.join([
        '        if cost < 0:',
        '            cost = 0',
        '        return cls(cost)',
    ]),
    '\n'.join([
        '        print("Creating house")',
        '        return cls(cost)',
    ]),
    '\n'.join([
        '        return cls(cost, [0])',
    ]),
    '\n'.join([
        '        return cls(cost + 10)',
    ]),
])
def test_invalid_classmethod(plugin_run, options_factory, ctor_body):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    @classmethod',
            '    def ctor(cls, cost):',
            ctor_body,
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert got == [(5, 8, 'PEO102 @classmethod should contain only cls() call')]


def test_classmethod_with_cls_call(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def create(cls, cost):',
            '        return cls(cost)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_classmethod_with_cls_call_two_args(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost, area):',
            '        self._cost = cost',
            '        self._area = area',
            '',
            '    @classmethod',
            '    def create(cls, cost, area):',
            '        return cls(cost, area)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_classmethod_with_cls_call_multiple_args(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost, area):',
            '        self._cost = cost',
            '        self._area = area',
            '',
            '    @classmethod',
            '    def create(cls, cost, area):',
            '        return cls(cost, area)',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got


def test_classmethod_with_return_without_value(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def create(cls, cost):',
            '        return',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert got == [(8, 8, 'PEO102 @classmethod should contain only cls() call')]


def test_classmethod_with_return_other_value(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def create(cls, cost):',
            '        return "invalid"',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert got == [(8, 8, 'PEO102 @classmethod should contain only cls() call')]


def test_classmethod_with_function_call(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    @classmethod',
            '    def create(cls, cost):',
            '        instance = cls(cost)',
            '        print("Creating house")',
            '        return instance',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert got == [
        (9, 8, 'PEO102 @classmethod should contain only cls() call'),
        (10, 8, 'PEO102 @classmethod should contain only cls() call'),
    ]


def test_regular_method_not_affected(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def __init__(self, cost):',
            '        self._cost = cost',
            '',
            '    def area(self) -> int:',
            '        if self._cost > 100:',
            '            return 5',
            '        return 3',
            '',
            '    def calculate(self):',
            '        result = self._cost * 2',
            '        return result',
        ]),
        [CodeFreeCtorVisitor(options_factory())]
    )

    assert not got

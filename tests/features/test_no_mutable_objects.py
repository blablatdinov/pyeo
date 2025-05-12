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

from pyeo.features.no_mutable_objects import NoMutableObjectsVisitor


@pytest.mark.parametrize('base_class', [
    'Protocol',
    'typing.Protocol',
    't.Protocol',
    't.Protocol, OtherClass',
    'OtherClass, Protocol',
    'OtherClass, t.Protocol',
    'Protocol[Mammal]',
    'Exception',
    'AppError',
    'TypedDict',
    'typing.TypedDict',
    't.TypedDict',
    'Enum',
])
def test_skip_with_base(plugin_run, base_class, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse({0}):'.format(base_class),
            '',
            '    def area(self) -> int: ...',
        ]),
        [NoMutableObjectsVisitor(options_factory())],
    )

    assert not got


@pytest.mark.parametrize('decorator', [
    '@attrs.define(frozen=True)',
    '@define(frozen=True)',
    '@attrs.frozen',
    '@frozen',
    '@attrs.frozen()',
    '@frozen()',
    '@dataclass(frozen=True)',
    '@dataclasses.dataclass(frozen=True)',
])
def test_valid(plugin_run, decorator, options_factory):
    got = plugin_run(
        '\n'.join([
            decorator,
            'class HttpHouse(House):',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoMutableObjectsVisitor(options_factory())],
    )

    assert not got


def test_invalid(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoMutableObjectsVisitor(options_factory())],
    )

    assert got == [(1, 0, 'PEO200 class must be frozen')]

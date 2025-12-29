# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

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

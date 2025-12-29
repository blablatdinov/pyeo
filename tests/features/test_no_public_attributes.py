# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

import pytest

from pyeo.features.no_public_attributes import NoPublicAttributesVisitor


@pytest.mark.parametrize('base_class', [
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
            '    name = "test"',
            '    def area(self) -> int: ...',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert not got


@pytest.mark.parametrize('base_class', [
    'Protocol',
    'typing.Protocol',
    't.Protocol',
    't.Protocol, OtherClass',
    'OtherClass, Protocol',
    'OtherClass, t.Protocol',
    'Protocol[Mammal]',
])
def test_protocol_with_public_attributes(plugin_run, base_class, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse({0}):'.format(base_class),
            '    name = "test"',
            '    value: int = 42',
            '    def area(self) -> int: ...',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert got == [
        (2, 4, 'PEO300 class attribute "name" should be private'),
        (3, 4, 'PEO300 class attribute "value" should be private'),
    ]


def test_valid_private_attributes(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    _private_attr = "test"',
            '    __very_private = "test"',
            '    _name: str = "test"',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert not got


def test_protocol_with_private_attributes(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(Protocol):',
            '    _private_attr = "test"',
            '    __very_private = "test"',
            '    _name: str = "test"',
            '',
            '    def area(self) -> int: ...',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert not got


def test_invalid_public_attributes_assign(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    name = "test"',
            '    value = 42',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert got == [
        (2, 4, 'PEO300 class attribute "name" should be private'),
        (3, 4, 'PEO300 class attribute "value" should be private'),
    ]


def test_invalid_public_attributes_ann_assign(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    name: str = "test"',
            '    value: int = 42',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert got == [
        (2, 4, 'PEO300 class attribute "name" should be private'),
        (3, 4, 'PEO300 class attribute "value" should be private'),
    ]


def test_mixed_public_private_attributes(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    _private_attr = "test"',
            '    public_attr = "test"',
            '    _private_typed: str = "test"',
            '    public_typed: int = 42',
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert got == [
        (3, 4, 'PEO300 class attribute "public_attr" should be private'),
        (5, 4, 'PEO300 class attribute "public_typed" should be private'),
    ]


def test_empty_class(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    pass',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert not got


def test_class_with_only_methods(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse:',
            '    def area(self) -> int:',
            '        return 5',
            '',
            '    def get_name(self) -> str:',
            '        return "house"',
        ]),
        [NoPublicAttributesVisitor(options_factory())],
    )

    assert not got

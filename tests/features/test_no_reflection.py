# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

import ast

import pytest

from pyeo.features.no_reflection import NoReflectionVisitor
from pyeo.main import Plugin


@pytest.mark.parametrize(('call', 'name'), [
    ('isinstance(box, list)', 'isinstance'),
    ('issubclass(Box, list)', 'issubclass'),
    ('type(box)', 'type'),
    ("hasattr(box, 'lid')", 'hasattr'),
    ("getattr(box, 'lid')", 'getattr'),
    ("setattr(box, 'lid', 1)", 'setattr'),
    ("delattr(box, 'lid')", 'delattr'),
    ('cast(int, box)', 'cast'),
    ('typing.cast(int, box)', 'cast'),
])
def test_reflection(plugin_run, options_factory, call, name):
    got = plugin_run(
        '\n'.join([
            'def size(box):',
            '    return {0}'.format(call),
        ]),
        [NoReflectionVisitor(options_factory())],
    )

    assert got == [(2, 11, 'PEO700 reflection is forbidden: {0}'.format(name))]


def test_class_pattern(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'def size(box):',
            '    match box:',
            '        case list():',
            '            return len(box)',
            '    return 0',
        ]),
        [NoReflectionVisitor(options_factory())],
    )

    assert got == [(3, 13, 'PEO700 reflection is forbidden: list')]


def test_nested_reflection(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'def size(box):',
            '    return len(box) if isinstance(box, list) else 0',
        ]),
        [NoReflectionVisitor(options_factory())],
    )

    assert got == [(2, 23, 'PEO700 reflection is forbidden: isinstance')]


@pytest.mark.parametrize('call', [
    "type('Box', (), {})",
    'box.cast(int)',
    'len(box)',
])
def test_valid(plugin_run, options_factory, call):
    got = plugin_run(
        '\n'.join([
            'def size(box):',
            '    return {0}'.format(call),
        ]),
        [NoReflectionVisitor(options_factory())],
    )

    assert not got


def test_plugin_reports_reflection(namespace_factory):
    Plugin.parse_options(namespace_factory())
    got = [
        viol[2]
        for viol in Plugin(
            ast.parse('\n'.join([
                'def size(box):',
                '    return isinstance(box, list)',
            ])),
        ).run()
    ]

    assert 'PEO700 reflection is forbidden: isinstance' in got

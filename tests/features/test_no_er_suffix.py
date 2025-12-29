# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

import pytest

from pyeo.features.no_er_suffix import NoErSuffix


@pytest.mark.parametrize('suffix', [
    'er',
])
def test_forbidden(plugin_run, suffix, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse{0}:'.format(suffix),
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoErSuffix(options_factory())],
    )

    assert got == [(1, 0, 'PEO300 "er" suffix forbidden')]


@pytest.mark.parametrize('suffix', [
    'User',
])
def test_whitelist(plugin_run, suffix, options_factory):
    got = plugin_run(
        '\n'.join([
            'class {0}(House):'.format(suffix),
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoErSuffix(options_factory())],
    )

    assert not got


@pytest.mark.parametrize('suffix', [
    'Answer',
])
def test_whitelist_from_options(plugin_run, suffix, options_factory):
    got = plugin_run(
        '\n'.join([
            'class Prefix{0}(House):'.format(suffix),
            '',
            '    def area(self) -> int:',
            '        return 5',
        ]),
        [NoErSuffix(options_factory([suffix]))],
    )

    assert not got

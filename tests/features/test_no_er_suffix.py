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

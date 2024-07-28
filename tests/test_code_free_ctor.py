# The MIT License (MIT).
#
# Copyright (c) 2023-2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
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

import ast

import pytest

from pyeo.main import Plugin


@pytest.fixture
def plugin_run():
    """Fixture for easy run plugin."""
    def _plugin_run(code: str) -> list[tuple[int, int, str]]:  # noqa: WPS430
        """Plugin run result."""
        plugin = Plugin(ast.parse(code))
        res = []
        for viol in plugin.run():
            res.append((
                viol[0],
                viol[1],
                viol[2],
            ))
        return res
    return _plugin_run


def test(plugin_run):
    got = plugin_run('\n'.join([
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
    ]))

    assert not got


def test_ctor_with_code(plugin_run):
    got = plugin_run('\n'.join([
        'class HttpHouse(House):',
        '',
        '    def __init__(self, cost):',
        '        self._cost = cost',
        '        if cost < 0:',
        '            self._cost = 0',
        '',
        '    @classmethod',
        '    def secondary_ctor(cls, cost):',
        '        return cls(cost)',
        '',
        '    def area(self) -> int:',
        '        return 5',
    ]))

    assert got == [(5, 8, 'PEO100 Ctor contain code')]

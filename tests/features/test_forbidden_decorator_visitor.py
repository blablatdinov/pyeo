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

from pyeo.features.forbidden_decorator_visitor import ForbiddenDecoratorVisitor


def test_valid(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def double_cost(self):',
            '        return self.cost * 2',
        ]),
        [ForbiddenDecoratorVisitor(options_factory())]
    )

    assert not got


def test_staticmethod(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    @staticmethod',
            '    def double_cost(cost):',
            '        return cost * 2',
        ]),
        [ForbiddenDecoratorVisitor(options_factory())]
    )

    assert got == [(4, 4, 'PEO400 Staticmethod is forbidden')]

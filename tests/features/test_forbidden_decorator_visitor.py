# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

import ast

from pyeo.features.forbidden_decorator_visitor import ForbiddenDecoratorVisitor
from pyeo.main import Plugin


def test_valid(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    def double_cost(self):',
            '        return self.cost * 2',
        ]),
        [ForbiddenDecoratorVisitor(options_factory())],
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
        [ForbiddenDecoratorVisitor(options_factory())],
    )

    assert got == [(4, 4, 'PEO400 Staticmethod is forbidden')]


def test_async_staticmethod(plugin_run, options_factory):
    got = plugin_run(
        '\n'.join([
            'class HttpHouse(House):',
            '',
            '    @staticmethod',
            '    async def double_cost(cost):',
            '        return cost * 2',
        ]),
        [ForbiddenDecoratorVisitor(options_factory())],
    )

    assert got == [(4, 4, 'PEO400 Staticmethod is forbidden')]


def test_plugin_reports_staticmethod(namespace_factory):
    Plugin.parse_options(namespace_factory())
    got = [
        viol[2]
        for viol in Plugin(
            ast.parse('\n'.join([
                'class HttpHouse(House):',
                '',
                '    @staticmethod',
                '    def double_cost(cost):',
                '        return cost * 2',
            ])),
        ).run()
    ]

    assert 'PEO400 Staticmethod is forbidden' in got

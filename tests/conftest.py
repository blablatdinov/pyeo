# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

import argparse
import ast

import attrs
import pytest

from pyeo.fk_plugin import FkPlugin
from pyeo.visitor_protocol import VisitorWithProblems


@attrs.define(frozen=True)
class _Options:

    available_er_names: list[str]


@pytest.fixture
def plugin_run():
    """Fixture for easy run plugin."""
    def _plugin_run(code: str, visitors: list[VisitorWithProblems]) -> list[tuple[int, int, str]]:  # noqa: WPS430
        """Plugin run result."""
        plugin = FkPlugin(ast.parse(code), visitors)
        return [
            (
                viol[0],
                viol[1],
                viol[2],
            )
            for viol in plugin.run()
        ]
    return _plugin_run


@pytest.fixture
def options_factory():
    def _options_factory(available_er_names: list[str] | None = None) -> _Options:  # noqa: WPS430
        if not available_er_names:
            available_er_names = []
        return _Options(available_er_names=available_er_names)
    return _options_factory


@pytest.fixture
def namespace_factory():
    def _namespace_factory(available_er_names: list[str] | None = None) -> argparse.Namespace:  # noqa: WPS430
        if not available_er_names:
            available_er_names = []
        return argparse.Namespace(available_er_names=available_er_names)
    return _namespace_factory

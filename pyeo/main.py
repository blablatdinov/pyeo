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

# flake8: noqa: WPS232

import argparse
import ast
from collections.abc import Generator
from typing import final

from flake8.options.manager import OptionManager

from pyeo.features.code_free_ctor_visitor import CodeFreeCtorVisitor
from pyeo.features.no_er_suffix import NoErSuffix
from pyeo.features.no_getter_methods import NoGetterMethodsVisitor
from pyeo.features.no_mutable_objects import NoMutableObjectsVisitor
from pyeo.features.no_property_decorator import NoPropertyDecoratorVisitor
from pyeo.features.no_public_attributes import NoPublicAttributesVisitor
from pyeo.visitor_protocol import VisitorWithProblems


@final
class Plugin:
    """Flake8 plugin."""

    _options: argparse.Namespace

    @classmethod
    def parse_options(cls, options: argparse.Namespace) -> None:
        """Parse registered options for providing them to each visitor."""
        cls._options = options

    def __init__(self, tree: ast.AST) -> None:
        """Ctor."""
        self._tree = tree
        self._visitors: list[VisitorWithProblems] = [
            CodeFreeCtorVisitor(self._options),
            NoMutableObjectsVisitor(self._options),
            NoErSuffix(self._options),
            NoPublicAttributesVisitor(self._options),
            NoPropertyDecoratorVisitor(self._options),
            NoGetterMethodsVisitor(self._options),
        ]

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Add command line options to the parser."""
        parser.add_option(
            long_option_name='--available-er-names',
            default=[],
            comma_separated_list=True,
            help='Available "er" names',
            parse_from_config=True,
        )

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        for visitor in self._visitors:
            visitor.visit(self._tree)
            for line in visitor.problems:  # noqa: WPS526
                yield (line[0], line[1], line[2], type(self))

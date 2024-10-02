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

"""NoErSuffix."""

import ast
from typing import final

from pyeo.utils.class_is_protocol import class_is_protocol


@final
class NoErSuffix(ast.NodeVisitor):
    """NoErSuffix."""

    def __init__(self, options) -> None:
        """Ctor."""
        self._options = options
        self.problems: list[tuple[int, int, str]] = []
        self._whitelist = {
            'User',
        } | set(self._options.available_er_names)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802, WPS231, C901
        """Visit by classes.

        :param node: ast.ClassDef
        """
        class_name = node.name
        if class_name.endswith('er'):
            for whitelist_suffix in self._whitelist:
                if class_name.endswith(whitelist_suffix):
                    break
            else:
                self.problems.append((node.lineno, node.col_offset, 'PEO300 "er" suffix forbidden'))
        self.generic_visit(node)

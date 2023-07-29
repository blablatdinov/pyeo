"""The MIT License (MIT).

Copyright (c) 2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from mypy.nodes import AssignmentStmt, Block, Decorator, FuncDef, NameExpr, PassStmt, ReturnStmt

from pyeo.utils.decorator_name import decorator_name


class NoCodeInCtorFeature(object):
    """Checking each object method has protocol."""

    def analyze(self, ctx) -> bool:
        """Analyzing.

        :param ctx: mypy context
        :return: bool
        """
        for func in ctx.cls.defs.body:
            if isinstance(func, Decorator) and 'classmethod' in {decorator_name(dec) for dec in func.original_decorators}:
                self._secondary_ctor_check(ctx, func)
            elif not isinstance(func, FuncDef):
                continue
            elif func.name == '__init__':
                self._primary_ctor_check(ctx, func)
        return True

    def _secondary_ctor_check(self, ctx, func):
        for elem in func.func.body.body:
            # TODO: ReturnStmt can contain logic like list comprehension
            # we must iter by nodes of expr and check all elements
            #
            # @classmethod
            # def secondary_ctor(cls, ages: list[str]):
            #     return cls(
            #         [int(x) for x in ages]
            #     )
            if not isinstance(elem, ReturnStmt):
                ctx.api.fail(
                    'Find code in ctor {0}.{1}.'.format(ctx.cls.name, func.name),
                    ctx.cls,
                )

    def _primary_ctor_check(self, ctx, func):
        for elem in func.body.body:
            if isinstance(elem, PassStmt):
                continue
            if not isinstance(elem, AssignmentStmt):
                ctx.api.fail(
                    'Find code in ctor {0}.{1}.'.format(ctx.cls.name, func.name),
                    ctx.cls,
                )

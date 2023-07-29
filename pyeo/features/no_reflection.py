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
from pprint import pprint

from mypy.nodes import Block, CallExpr


class NoReflectionFeature(object):
    """Checking each object method has protocol."""

    def analyze(self, ctx) -> bool:
        """Analyzing.

        :param ctx: mypy context
        :return: bool
        """
        for elem in ctx.cls.defs.body:
            self._walk_expressions(ctx, elem)
        return True

    def _walk_expressions(self, ctx, expr):
        forbid_func_names = (
            'builtins.isinstance',
            'builtins.type',
            'builtins.issubclass',
            'builtins.hasattr',
        )
        if hasattr(expr, 'body'):
            self._walk_expressions(ctx, expr.body)
        if isinstance(expr, list):
            for elem in expr:
                self._walk_expressions(ctx, elem)
        if hasattr(expr, 'expr'):
            self._walk_expressions(ctx, expr.expr)
        if isinstance(expr, CallExpr):
            if expr.callee.fullname in forbid_func_names:
                ctx.api.fail(
                    "Class '{0}' has '{1}' reflection function call.".format(
                        ctx.cls.name,
                        expr.callee.fullname,
                    ),
                    ctx.cls,
                )
            if hasattr(expr, 'args'):
                for elem in expr.args:
                    self._walk_expressions(ctx, elem)
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
from mypy.nodes import AssignmentStmt, EllipsisExpr, ExpressionStmt, FuncDef, PassStmt, StrExpr


class ProtocolMethodCodeFreeFeature(object):
    """Check protocol methods code free."""

    def analyze(self, ctx) -> bool:  # noqa: WPS231 need in refactor
        """Analyzing.

        :param ctx: mypy context
        :return: bool
        """
        for method in ctx.cls.defs.body:
            if not isinstance(method, FuncDef):
                continue
            for body_item in method.body.body:
                fail_args = ("Protocol '{0}' method '{1}' has implementation".format(ctx.cls.name, method.name), ctx.cls)
                if isinstance(body_item, PassStmt):
                    continue
                if not hasattr(body_item, 'expr'):  # noqa: WPS421 need in refactor
                    ctx.api.fail(*fail_args)
                    continue
                if not isinstance(body_item.expr, (EllipsisExpr, StrExpr)):
                    ctx.api.fail(*fail_args)
        return True

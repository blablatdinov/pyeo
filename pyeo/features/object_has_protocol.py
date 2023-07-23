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


class ObjectHasProtocolFeature(object):
    """Check object has protocol."""

    def analyze(self, ctx) -> bool:
        """Analyzing.

        :param ctx: mypy context
        :return: bool
        """
        if not ctx.cls.base_type_exprs:
            ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)
            return False
        base_type_exprs = ctx.cls.base_type_exprs[0]
        for node in base_type_exprs.node.mro:
            if node.is_protocol:
                return True
        ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)
        return False

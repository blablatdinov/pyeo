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
from mypy.nodes import Decorator, FuncDef


class EachMethodHasProtocolFeature(object):
    """Checking each object method has protocol."""

    def analyze(self, ctx) -> bool:
        """Analyzing.

        :param ctx: mypy context
        :return: bool
        """
        object_methods = {
            def_body.name: def_body
            for def_body in ctx.cls.defs.body
            if isinstance(def_body, FuncDef) and not def_body.name.startswith('_') and not self._method_is_ctor(def_body)
        }
        if not ctx.cls.base_type_exprs:
            return False
        extra_method_names = set(object_methods.keys()) - {  # noqa: WPS224 need a refactor
            method.name
            for base_type in ctx.cls.base_type_exprs
            for node in base_type.node.mro
            for method in node.defn.defs.body
            if isinstance(method, FuncDef)
        }
        if extra_method_names:
            failed_methods = [
                method
                for method_name, method in object_methods.items()
                if method_name in extra_method_names
            ]
            for method in failed_methods:
                ctx.api.fail(
                    "Class '{0}' have public extra method '{1}' without protocol.".format(
                        ctx.cls.name,
                        method.name,
                    ),
                    method,
                )
        return True

    def _method_is_ctor(self, def_body) -> bool:
        if not isinstance(def_body, Decorator):
            return False
        for dec in def_body.original_decorators:
            if dec.name == 'classmethod':
                return True
        return False

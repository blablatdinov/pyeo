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
from mypy.plugin import Plugin

from pyeo.features.final_object import FinalClassFeature
from pyeo.features.method_has_protocol import EachMethodHasProtocolFeature
from pyeo.features.object_has_protocol import ObjectHasProtocolFeature
from pyeo.features.protocol_method_code_free import ProtocolMethodCodeFreeFeature


def analyze(ctx):
    """Features controller.

    :param ctx: mypy context
    :return: bool
    """
    if ctx.cls.removed_base_type_exprs and ctx.cls.removed_base_type_exprs[0].fullname == 'typing.Protocol':
        ProtocolMethodCodeFreeFeature().analyze(ctx)
        return True
    if not ObjectHasProtocolFeature().analyze(ctx):
        return True
    EachMethodHasProtocolFeature().analyze(ctx)
    FinalClassFeature().analyze(ctx)
    return True


class CustomPlugin(Plugin):
    """Our plugin for mypy."""

    def get_class_decorator_hook_2(self, fullname: str):  # noqa: WPS114 mypy api
        """Hook for find elegant objects.

        :param fullname: str
        :return: analyze
        """
        if fullname == 'pyeo.elegant':
            return analyze


def plugin(version: str):
    """Plugin entrypoint.

    :param version: str
    :return: CustomPlugin
    """
    return CustomPlugin

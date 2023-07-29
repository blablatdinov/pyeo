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
from mypy.nodes import IndexExpr
from mypy.plugin import Plugin

from pyeo.features.final_object import FinalClassFeature
from pyeo.features.method_has_protocol import EachMethodHasProtocolFeature
from pyeo.features.no_code_in_ctors import NoCodeInCtorFeature
from pyeo.features.no_er_names import NoErNamesFeature
from pyeo.features.no_property_methods import NoPropertyMethodsFeature
from pyeo.features.no_reflection import NoReflectionFeature
from pyeo.features.no_setters import NoSettersFeature
from pyeo.features.no_staticmethods import NoStaticmethodsFeature
from pyeo.features.object_has_protocol import ObjectHasProtocolFeature
from pyeo.features.protocol_method_code_free import ProtocolMethodCodeFreeFeature


def _is_protocl(cls):
    if not cls.removed_base_type_exprs:
        return False
    if isinstance(cls.removed_base_type_exprs[0], IndexExpr):
        return cls.removed_base_type_exprs[0].base.fullname == 'typing.Protocol'
    return cls.removed_base_type_exprs[0].fullname == 'typing.Protocol'


def analyze(ctx):
    """Features controller.

    :param ctx: mypy context
    :return: bool
    """
    # print(ctx.cls.fullname)
    # # print(ctx.cls.removed_base_type_exprs)
    # for x in ctx.cls.removed_base_type_exprs:
    #     print(x)
    # print('\n' * 3)
    if _is_protocl(ctx.cls):
        NoPropertyMethodsFeature().analyze(ctx)
        ProtocolMethodCodeFreeFeature().analyze(ctx)
        NoSettersFeature().analyze(ctx)
        NoStaticmethodsFeature().analyze(ctx)
        return True
    if not ObjectHasProtocolFeature().analyze(ctx):
        return True
    EachMethodHasProtocolFeature().analyze(ctx)
    FinalClassFeature().analyze(ctx)
    NoErNamesFeature().analyze(ctx)
    NoPropertyMethodsFeature().analyze(ctx)
    NoSettersFeature().analyze(ctx)
    NoCodeInCtorFeature().analyze(ctx)
    NoStaticmethodsFeature().analyze(ctx)
    NoReflectionFeature().analyze(ctx)
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

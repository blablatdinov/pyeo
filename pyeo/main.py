"""No object without interface."""
from mypy.plugin import Plugin
from pyeo._features.object_has_protocol import ObjectHasProtocolFeature
from pyeo._features.method_has_protocol import EachMethodHasProtocolFeature
from pyeo._features.protocol_method_code_free import ProtocolMethodCodeFreeFeature


def analyze(ctx):
    if ctx.cls.removed_base_type_exprs and ctx.cls.removed_base_type_exprs[0].fullname == 'typing.Protocol':
        ProtocolMethodCodeFreeFeature().analyze(ctx)
        return True
    if not ObjectHasProtocolFeature().analyze(ctx):
        return True
    EachMethodHasProtocolFeature().analyze(ctx)
    return True


class CustomPlugin(Plugin):

    def get_class_decorator_hook_2(self, fullname: str):
        if fullname == 'pyeo.elegant':
            return analyze


def plugin(version: str):
    return CustomPlugin

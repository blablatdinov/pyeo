"""No object without interface."""
from mypy.plugin import Plugin


def _has_protocol(ctx) -> bool:
    if len(ctx.cls.base_type_exprs) == 0:
        return False
    for node in ctx.cls.base_type_exprs[0].node.mro:
        if node.is_protocol:
            return True
    return False


def analyze(ctx):
    if not _has_protocol(ctx):
        ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)
    return True


class CustomPlugin(Plugin):

    def get_class_decorator_hook_2(self, fullname: str):
        if fullname == 'pyeo.elegant':
            return analyze


def plugin(version: str):
    return CustomPlugin

"""No object without interface."""
from mypy.plugin import Plugin


def _has_protocol(ctx) -> bool:
    if len(ctx.cls.base_type_exprs) == 0:
        return False
    for node in ctx.cls.base_type_exprs[0].node.mro:
        if node.is_protocol:
            return True
    return False


def _each_method_has_protocol(ctx) -> bool:
    methods_list = [
        def_body
        for def_body in ctx.cls.defs.body
        if not def_body.name.startswith('_')
    ]
    if not ctx.cls.base_type_exprs:
        return False
    protocol_methods = [
        method
        for base_type in ctx.cls.base_type_exprs
        for node in base_type.node.mro
        for method in node.defn.defs.body
    ]
    extra_method_names = set(m.name for m in methods_list) - set(m.name for m in protocol_methods)
    if extra_method_names:
        for extra_method_name in extra_method_names:
            method = [x for x in methods_list if extra_method_name == x.name][0]
            ctx.api.fail(
                "Class '{0}' have public extra method '{1}' without protocol.".format(
                    ctx.cls.name,
                    method.name,
                ),
                method,
            )
    return True


def analyze(ctx):
    if not _has_protocol(ctx):
        ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)
        return True
    _each_method_has_protocol(ctx)
    return True


class CustomPlugin(Plugin):

    def get_class_decorator_hook_2(self, fullname: str):
        if fullname == 'pyeo.elegant':
            return analyze


def plugin(version: str):
    return CustomPlugin

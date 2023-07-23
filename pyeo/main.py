"""No object without interface."""
from mypy.plugin import Plugin
from mypy.nodes import EllipsisExpr, PassStmt, StrExpr


def _has_protocol(ctx) -> bool:
    if len(ctx.cls.base_type_exprs) == 0:
        return False
    for node in ctx.cls.base_type_exprs[0].node.mro:
        if node.is_protocol:
            return True
    return False


def _each_method_has_protocol(ctx) -> bool:
    object_methods = {
        def_body.name: def_body
        for def_body in ctx.cls.defs.body
        if not def_body.name.startswith('_')
    }
    if not ctx.cls.base_type_exprs:
        return False
    protocol_methods = set(
        method.name
        for base_type in ctx.cls.base_type_exprs
        for node in base_type.node.mro
        for method in node.defn.defs.body
    )
    extra_method_names = set(object_methods.keys()) - protocol_methods
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


def _protocol_method_code_free(ctx):
    for method in ctx.cls.defs.body:
        for body_item in method.body.body:
            if isinstance(body_item, PassStmt):
                continue
            if not hasattr(body_item, 'expr'):
                ctx.api.fail("Protocol '{0}' method '{1}' has implementation".format(ctx.cls.name, method.name), ctx.cls)
                continue
            if not isinstance(body_item.expr, (EllipsisExpr, StrExpr)):
                ctx.api.fail("Protocol '{0}' method '{1}' has implementation".format(ctx.cls.name, method.name), ctx.cls)


def analyze(ctx):
    if ctx.cls.removed_base_type_exprs and ctx.cls.removed_base_type_exprs[0].fullname == 'typing.Protocol':
        _protocol_method_code_free(ctx)
        return True
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

from mypy.nodes import EllipsisExpr, PassStmt, StrExpr


class ProtocolMethodCodeFreeFeature(object):

    def analyze(self, ctx) -> bool:
        for method in ctx.cls.defs.body:
            for body_item in method.body.body:
                if isinstance(body_item, PassStmt):
                    continue
                if not hasattr(body_item, 'expr'):
                    ctx.api.fail("Protocol '{0}' method '{1}' has implementation".format(ctx.cls.name, method.name), ctx.cls)
                    continue
                if not isinstance(body_item.expr, (EllipsisExpr, StrExpr)):
                    ctx.api.fail("Protocol '{0}' method '{1}' has implementation".format(ctx.cls.name, method.name), ctx.cls)
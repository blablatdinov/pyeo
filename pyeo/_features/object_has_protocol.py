class ObjectHasProtocolFeature(object):

    def analyze(self, ctx) -> bool:
        if len(ctx.cls.base_type_exprs) == 0:
            ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)
            return False
        for node in ctx.cls.base_type_exprs[0].node.mro:
            if node.is_protocol:
                return True
        ctx.api.fail("Class '{0}' does not implement a Protocol.".format(ctx.cls.name), ctx.cls)

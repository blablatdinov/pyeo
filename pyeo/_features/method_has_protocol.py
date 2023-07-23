class EachMethodHasProtocolFeature(object):

    def analyze(self, ctx) -> bool:
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
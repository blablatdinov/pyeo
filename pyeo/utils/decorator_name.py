from mypy.nodes import AssignmentStmt, Block, CallExpr, Decorator, FuncDef, NameExpr, PassStmt, ReturnStmt


def decorator_name(item):
    if isinstance(item, NameExpr):
        return item.name
    elif isinstance(item, CallExpr):
        return item.callee.fullname

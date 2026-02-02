import ast

from variable_declaration_checker.variable_scope import VariableScope
from variable_declaration_checker.visit_result import VisitResult


class VariableDeclarationVisitor(ast.NodeVisitor):
    def __init__(self):
        self.__result_un_declared: list[VisitResult] = []
        self.__result_re_declared: list[VisitResult] = []
        self.__current_scope: VariableScope = VariableScope(None, False, False, False)

    def get_visit_result(self, clear: bool = True):
        un_declared: list[VisitResult]  = self.__result_un_declared
        re_declared: list[VisitResult]  = self.__result_re_declared
        if clear:
            self.__result_un_declared = []
            self.__result_re_declared = []
            return un_declared, re_declared
        else:
            return list(un_declared), list(re_declared)

    def __found_variable(self, node: ast.Name, annotated: bool):
        self.__found_variable_any_node(node, annotated, node.id)

    def __found_variable_any_node(self, 
                                  node: ast.Name | ast.excepthandler | ast.pattern | ast.stmt | ast.arg, 
                                  annotated: bool, 
                                  variable: str):
        if annotated:
            if self.__current_scope.declare_variable(variable):
                self.__result_re_declared.append({
                    "name": variable,
                    "col_offset": node.col_offset,
                    "lineno": node.lineno
                })
            return
        
        if self.__current_scope.assign_variable(variable):
            self.__result_un_declared.append({
                    "name": variable,
                    "col_offset": node.col_offset,
                    "lineno": node.lineno
                })

    def visit_Module(self, node: ast.Module):
        self.__current_scope = self.__current_scope.create_sub_scope(False, False, False)
        self.generic_visit(node)
        self.__current_scope = self.__current_scope.get_parent_scope()

    def visit_NamedExpr(self, node: ast.NamedExpr):
        self.__found_variable(node.target, False)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        return
    
    def visit_SetComp(self, node: ast.SetComp):
        return

    def visit_DictComp(self, node: ast.DictComp):
        return

    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        return

    # TODO: Consider self.xxxx
    def visit_Assign(self, node: ast.Assign):
        def deal_target(target: ast.expr):
            if isinstance(target, ast.Name):
                self.__found_variable(target, self.__current_scope.is_enum_class())
            elif isinstance(target, ast.Tuple | ast.List):
                for target in target.elts:
                    deal_target(target)
            elif isinstance(target, ast.Starred):
                deal_target(target.value)

        target: ast.expr
        for target in node.targets:
            deal_target(target)
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            self.__found_variable(node.target, True)
        self.generic_visit(node)
    
    def visit_Delete(self, node: ast.Delete):
        def deal_target(target: ast.expr):
            if isinstance(target, ast.Name):
                self.__current_scope.remove_variable(target.id)
            elif isinstance(target, ast.Tuple | ast.List):
                for target in target.elts:
                    deal_target(target)

        target: ast.expr
        for target in node.targets:
            deal_target(target)
        self.generic_visit(node)
    
    def visit_TypeAlias(self, node: ast.TypeAlias):
        self.__found_variable(node.name, True)
        self.generic_visit(node)

    def visit_For(self, node: ast.For | ast.AsyncFor):
        def deal_target(target: ast.expr):
            if isinstance(target, ast.Name):
                self.__found_variable(target, False)
            elif isinstance(target, ast.Tuple | ast.List):
                for target in target.elts:
                    deal_target(target)
            elif isinstance(target, ast.Starred):
                deal_target(target.value)

        deal_target(node.target)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name is not None:
            self.__found_variable_any_node(node, False, node.name)
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem):
        def deal_target(target: ast.expr | None):
            if isinstance(target, ast.Name):
                self.__found_variable(target, False)
            elif isinstance(target, ast.Tuple | ast.List):
                for target in target.elts:
                    deal_target(target)
            elif isinstance(target, ast.Starred):
                deal_target(target.value)

        deal_target(node.optional_vars)
        self.generic_visit(node)
    
    def visit_MatchStar(self, node: ast.MatchStar):
        if node.name is not None:
            self.__found_variable_any_node(node, False, node.name)
        self.generic_visit(node)
    
    def visit_MatchMapping(self, node: ast.MatchMapping):
        if node.rest is not None:
            self.__found_variable_any_node(node, False, node.rest)
        self.generic_visit(node)
    
    def visit_MatchAs(self, node: ast.MatchAs):
        if node.name is not None:
            self.__found_variable_any_node(node, False, node.name)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        self.__found_variable_any_node(node, True, node.name)

        is_self: bool = self.__current_scope.is_class()

        self.__current_scope = self.__current_scope.create_sub_scope(False, False, node.name == "__init__")
        
        if is_self:
            decorator: ast.expr
            for decorator in node.decorator_list:
                if not isinstance(decorator, ast.Name):
                    continue
                if decorator.id == "staticmethod":
                    is_self = False
                    break

        def deal_arg(node: ast.arg | None):
            if node is None:
                return
            
            nonlocal is_self

            self.__found_variable_any_node(node, 
                                           is_self or (node.annotation is not None), 
                                           node.arg)
            
            if is_self:
                is_self = False
            
        argument: ast.arg
        for argument in node.args.posonlyargs:
            deal_arg(argument)
        for argument in node.args.args:
            deal_arg(argument)
        for argument in node.args.kwonlyargs:
            deal_arg(argument)
        deal_arg(node.args.vararg)
        deal_arg(node.args.kwarg)

        self.generic_visit(node)
        self.__current_scope = self.__current_scope.get_parent_scope()

    def visit_Global(self, node: ast.Global | ast.Nonlocal):
        name: str
        for name in node.names:
            self.__found_variable_any_node(node, True, name)
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        self.visit_Global(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.__found_variable_any_node(node, True, node.name)
        
        is_enum: bool = False
        enum_bases: set[str] = {"Enum", "IntEnum", "StrEnum", "Flag", "IntFlag", "ReprEnum"}
        base: ast.expr
        for base in node.bases:
            if isinstance(base, ast.Name):
                if base.id in enum_bases:
                    is_enum = True
                    break
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name):
                if (base.value.id == "enum") and (base.attr in enum_bases):
                    is_enum = True
                    break

        self.__current_scope = self.__current_scope.create_sub_scope(True, is_enum, False)

        self.generic_visit(node)
        self.__current_scope = self.__current_scope.get_parent_scope()
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)
    
    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.visit_For(node)

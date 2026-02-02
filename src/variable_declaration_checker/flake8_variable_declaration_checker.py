import ast
from variable_declaration_checker.variable_declaration_visitor import VariableDeclarationVisitor
from variable_declaration_checker.visit_result import VisitResult

class Flake8VariableDeclarationChecker:
    def __init__(self, tree: ast.AST):
        self.__tree = tree

    def run(self):
        visitor: VariableDeclarationVisitor = VariableDeclarationVisitor()
        visitor.visit(self.__tree)

        un_declared: list[VisitResult]
        re_declared: list[VisitResult]
        un_declared, re_declared = visitor.get_visit_result()

        node: VisitResult
        for node in un_declared:
            yield (
                node["lineno"],
                node["col_offset"],
                f"WVarDec01 Declare the variable '{node["name"]}' with type annotation before use.",
                Flake8VariableDeclarationChecker
            )

        for node in re_declared:
            yield (
                node["lineno"],
                node["col_offset"],
                f"WVarDec02 The variable '{node["name"]}' is declared twice. Rename it or 'del' it if needed.",
                Flake8VariableDeclarationChecker
            )

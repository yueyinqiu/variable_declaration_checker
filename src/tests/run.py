import ast

from variable_declaration_checker import Flake8VariableDeclarationChecker

print(ast.dump(ast.parse(
"""
class CLASS:
    def FUNC(self, a):
        pass
"""), indent=4))
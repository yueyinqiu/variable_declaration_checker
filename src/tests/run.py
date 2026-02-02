import ast
import enum

from variable_declaration_checker import Flake8VariableDeclarationChecker
class CLASS(enum.Enum):
    x = 1

y = 2
print(ast.dump(ast.parse(
"""
class CLASS(enum.Enum):
    (x, y) = 1
"""), indent=4))
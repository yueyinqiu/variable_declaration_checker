# variable_declaration_checker

> We have migrated to Flake8 as Pylint's performance becomes a bottleneck on larger projects. Since our workflow focuses on file-by-file linting rather than cross-module dependency checks, Flake8 is a better fit. If you still prefer Pylint, use `variable-declaration-checker==0.0.7`.

## Installation and Basic Usage

```shell
pip install variable-declaration-checker
flake8 --select WVarDec
```

## Special Cases

We want this plugin to work with Visual Studio Code. Therefore, all behaviors that conflict with Pylance need to be eliminated. For example, if you find that not adding type annotations causes warnings from this plugin, while adding type annotations causes errors in Pylance, please report it to us.

Note that `ast` does not provide complete type information. This makes it impossible to implement some functions. We may need to expand or narrow the scope of the inspection. The specially handled cases are described below.

### `self` and `cls`

The first argument of a method (`self`, or `cls` for class method) is considered unnecessary to be declared:

```python
# This won't affect the functions that are not defined in a class.
def f1(self):    # WVarDec01 Declare the variable 'self' with type annotation before use.
    pass

class MyClass:
    def f2(self):    # No warning.
        pass
    
    # It check the argument's name and position at the same time:
    # Only the first argument that named "self" or "cls" will considered unnecessary to be declared.
    # This design is to deal with decorators like @staticmethod.

    # This won't be a problem if you use it with Pylance,
    # as Pylance will require you to rename the argument to "self" or "cls" (with a warning).
    # So as you fix the problems in Pylance, the plugin will work as expected.

    def f3(x):    # WVarDec01 Declare the variable 'x' with type annotation before use. Pylance: Instance methods should take a "self" parameter
        pass

    @staticmethod
    def f4(self):    # No warning. However Pylance: Static methods should not take a "self" or "cls"
        pass
```

### Underscores

Underscores (or discards, `_`) will simply be ignored.

```python
x = ""    # WVarDec01 Declare the variable 'x' with type annotation before use.
x: str = ""    # WVarDec02 The variable 'x' is declared twice. Rename it or 'del' it if needed.

_ = ""    # No warning
_: str = ""    # Still no warning
```

### Enums

If you use type annotation for enum members, Pylance will say "Type annotations are not allowed for enum members". So the checker will skip for enum numbers. However, due to the limitations of `ast`, we can only roughly determine whether a type is an Enum by its base class name:

```python
from enum import Enum, IntFlag
import enum

class NotE:
    X = 1    # WVarDec01 Declare the variable 'X' with type annotation before use.

class NotE2:
    X: int = 1    # No warnings.

class E1(Enum):
    X: int = 1    # No warnings. However Pylance: Type annotations are not allowed for enum members

class E2(Enum):
    X = 1    # No warnings.

# Supports "Enum", "IntEnum", "StrEnum", "Flag", "IntFlag" and "ReprEnum"
class E3(IntFlag):
    X = 1    # No warnings.

# Supports "enum.Enum", "enum.IntEnum", "enum.StrEnum", "enum.Flag", "enum.IntFlag" and "enum.ReprEnum"
class E4(enum.Flag):
    X = 1    # No warnings.

# FAIL CASES: It can't know the actual class and can only detect by the class name.

# It is not an Enum but
class ReprEnum: pass
class E5(ReprEnum):
    X = 1    # No warnings.

# It is an Enum but
class E6(E1):
    Y = 1    # WVarDec01 Declare the variable 'Y' with type annotation before use.
```

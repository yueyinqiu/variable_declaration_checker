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
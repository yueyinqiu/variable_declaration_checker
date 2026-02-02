from typing import TypedDict


class VisitResult(TypedDict):
    lineno: int
    col_offset: int
    name: str
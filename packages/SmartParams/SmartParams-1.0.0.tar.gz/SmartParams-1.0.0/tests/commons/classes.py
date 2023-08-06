from dataclasses import dataclass, field
from typing import Any, Type

from smartparams import Smart


@dataclass
class ParentA:
    arg1: str
    arg2: int = 5


@dataclass
class ChildA(ParentA):
    arg3: tuple[bool] = (True,)
    arg4: dict[int, str] = field(default_factory=lambda: {1: 'one'})


@dataclass
class ParentB:
    smart: Smart
    smart_a: Smart[ParentA]
    object_a: ParentA
    type_a: Type[ParentA]
    any_type: Any


class ParentC:
    def __init__(
        self,
        only_positional: str,
        /,
        positional: str,
        *args: bool,
        keyword: float,
        **kwargs: bytes,
    ) -> None:
        self.only_positional = only_positional
        self.positional = positional
        self.args = args
        self.keyword = keyword
        self.kwargs = kwargs


class RaiseClass:
    def __init__(self) -> None:
        raise RuntimeError


def some_function() -> None:
    pass


def square(x: int) -> int:
    return x**2


def to_upper_case(x: str) -> str:
    return x.upper()


def equation(
    a: str,
    /,
    b: int = 10,
) -> str:
    return f"{a}={b}"


def any_type_function(  # type: ignore
    a: str,
    b,
    *c: bool,
    d=10,
    **e: float,
) -> bytes:
    ...

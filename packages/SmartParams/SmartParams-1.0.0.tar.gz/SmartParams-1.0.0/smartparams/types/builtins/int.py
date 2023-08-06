from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return 'int' + self.missing_value


def simplifier(
    self: SmartRegister,
    default: int,
    skip_default: bool,
    strict: bool,
) -> int:
    return default


def register() -> None:
    Smart.register(
        cls=int,
        class_schema=class_schema,
        simplifier=simplifier,
    )

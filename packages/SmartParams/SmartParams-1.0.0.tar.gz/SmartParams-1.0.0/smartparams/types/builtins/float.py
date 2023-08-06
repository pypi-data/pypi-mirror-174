from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return 'float' + self.missing_value


def simplifier(
    self: SmartRegister,
    default: float,
    skip_default: bool,
    strict: bool,
) -> float:
    return default


def register() -> None:
    Smart.register(
        cls=float,
        class_schema=class_schema,
        simplifier=simplifier,
    )

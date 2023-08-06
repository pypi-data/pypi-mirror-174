from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return 'bool' + self.missing_value


def simplifier(
    self: SmartRegister,
    default: bool,
    skip_default: bool,
    strict: bool,
) -> bool:
    return default


def register() -> None:
    Smart.register(
        cls=bool,
        class_schema=class_schema,
        simplifier=simplifier,
    )

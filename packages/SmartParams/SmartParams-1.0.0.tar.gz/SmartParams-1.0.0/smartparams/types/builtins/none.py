from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> None:
    return None


def simplifier(
    self: SmartRegister,
    default: None,
    skip_default: bool,
    strict: bool,
) -> None:
    return default


def register() -> None:
    Smart.register(
        cls=type(None),
        class_schema=class_schema,
        simplifier=simplifier,
    )

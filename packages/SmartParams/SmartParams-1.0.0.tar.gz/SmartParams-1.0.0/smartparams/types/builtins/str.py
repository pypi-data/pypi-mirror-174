from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return 'str' + self.missing_value


def instance_schema(
    self: SmartRegister,
    instance: str,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return instance


def simplifier(
    self: SmartRegister,
    default: str,
    skip_default: bool,
    strict: bool,
) -> str:
    return default


def register() -> None:
    Smart.register(
        cls=str,
        class_schema=class_schema,
        instance_schema=instance_schema,
        simplifier=simplifier,
    )

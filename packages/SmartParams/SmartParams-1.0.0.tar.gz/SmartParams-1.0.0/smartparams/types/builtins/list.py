from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> list:
    return []


def simplifier(
    self: SmartRegister,
    default: list,
    skip_default: bool,
    strict: bool,
) -> list:
    return [self.simplify(item, skip_default, strict) for item in default]


def smartifier(
    self: SmartRegister,
    obj: list,
) -> list:
    return [self.smartify(item) for item in obj]


def from_list(
    self: SmartRegister,
    argument: list,
    subtypes: tuple[Any],
) -> list:
    expected_type = subtypes[0] if subtypes else Any
    return [self.convert(item, expected_type) for item in argument]


def register() -> None:
    Smart.register(
        cls=list,
        class_schema=class_schema,
        simplifier=simplifier,
        smartifier=smartifier,
        converter={
            list: from_list,
        },
    )

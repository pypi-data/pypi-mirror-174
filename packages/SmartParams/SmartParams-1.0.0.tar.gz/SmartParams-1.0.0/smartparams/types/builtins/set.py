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
    default: set,
    skip_default: bool,
    strict: bool,
) -> list:
    return [self.simplify(item, skip_default, strict) for item in default]


def from_list(
    self: SmartRegister,
    argument: list,
    subtypes: tuple[()] | tuple[Any],
) -> set:
    expected_type = subtypes[0] if subtypes else Any
    return {self.convert(item, expected_type) for item in argument}


def register() -> None:
    Smart.register(
        cls=set,
        class_schema=class_schema,
        simplifier=simplifier,
        converter={
            list: from_list,
        },
    )

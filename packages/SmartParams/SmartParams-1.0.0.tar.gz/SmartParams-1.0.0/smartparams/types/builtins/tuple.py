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
    default: tuple,
    skip_default: bool,
    strict: bool,
) -> list:
    return [self.simplify(item, skip_default, strict) for item in default]


def from_list(
    self: SmartRegister,
    argument: list,
    subtypes: tuple[Any, ...],
) -> tuple:
    if len(subtypes) > 1 and subtypes[-1] is ...:
        expected_types = (subtypes[0],) * len(argument)
    else:
        expected_types = subtypes + (Any,) * (len(argument) - len(subtypes))
    return tuple(
        self.convert(item, expected_type) for item, expected_type in zip(argument, expected_types)
    )


def register() -> None:
    Smart.register(
        cls=tuple,
        class_schema=class_schema,
        simplifier=simplifier,
        converter={
            list: from_list,
        },
    )

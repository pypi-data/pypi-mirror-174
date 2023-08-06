from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> dict:
    return {}


def simplifier(
    self: SmartRegister,
    default: dict,
    skip_default: bool,
    strict: bool,
) -> dict:
    return {k: self.simplify(v, skip_default, strict) for k, v in default.items()}


def smartifier(
    self: SmartRegister,
    obj: dict,
) -> dict | Smart:
    if all(isinstance(k, str) for k in obj):
        return Smart(**obj)
    return {k: self.smartify(v) for k, v in obj.items()}


def from_smart(
    self: SmartRegister,
    argument: Smart,
    subtypes: tuple[Any],
) -> dict:
    expected_type = subtypes[0] if subtypes else Any
    return {k: self.convert(v, expected_type) for k, v in argument.items()}


def from_dict(
    self: SmartRegister,
    argument: dict,
    subtypes: tuple[Any, Any],
) -> dict:
    _, expected_type = subtypes
    return {k: self.convert(v, expected_type) for k, v in argument.items()}


def register() -> None:
    Smart.register(
        cls=dict,
        class_schema=class_schema,
        simplifier=simplifier,
        smartifier=smartifier,
        converter={
            Smart: from_smart,
            dict: from_dict,
        },
    )

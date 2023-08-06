from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> dict:
    if subtypes:
        return self.schema(
            annotation=subtypes[0],
            skip_default=skip_default,
        )
    return {}


def simplifier(
    self: SmartRegister,
    default: Smart,
    skip_default: bool,
    strict: bool,
) -> dict:
    return {k: default.register.simplify(v, skip_default, strict) for k, v in default.items()}


def from_smart(
    self: SmartRegister,
    argument: Smart,
    subtypes: tuple[Any, ...],
) -> Smart:
    return argument.with_class(subtypes)


def from_str(
    self: SmartRegister,
    argument: str,
    subtypes: tuple[Any, ...],
) -> Smart:
    return Smart(argument).with_class(subtypes)


def register() -> None:
    Smart.register(
        cls=Smart,
        class_schema=class_schema,
        simplifier=simplifier,
        converter={
            Smart: from_smart,
            str: from_str,
        },
    )

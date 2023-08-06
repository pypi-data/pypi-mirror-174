from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return self.missing_value


def from_smart(
    self: SmartRegister,
    argument: Smart,
    subtypes: tuple[Any, ...],
) -> Any:
    return argument.with_class(subtypes)()


def register() -> None:
    Smart.register(
        cls=Any,
        class_schema=class_schema,
        converter={
            Smart: from_smart,
        },
    )

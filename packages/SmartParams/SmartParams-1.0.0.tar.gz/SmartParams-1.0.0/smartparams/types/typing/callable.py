from typing import Any, Callable

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> Any:
    return 'callable' + self.missing_value


def simplifier(
    self: SmartRegister,
    default: Callable,
    skip_default: bool,
    strict: bool,
) -> str:
    return self.class_path(default)


def from_str(
    self: SmartRegister,
    argument: str,
    subtypes: tuple[Any, ...],
) -> Callable:
    return self.import_class(argument)


def from_smart(
    self: SmartRegister,
    argument: Smart,
    subtypes: tuple[Any, ...],
) -> Callable:
    return argument.cls


def register() -> None:
    Smart.register(
        cls=Callable,
        class_schema=class_schema,
        simplifier=simplifier,
        converter={
            str: from_str,
            Smart: from_smart,
        },
    )

from typing import Any, ForwardRef

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def instance_schema(
    self: SmartRegister,
    instance: Any,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return instance.__forward_arg__


def register() -> None:
    Smart.register(
        cls=ForwardRef,
        instance_schema=instance_schema,
    )

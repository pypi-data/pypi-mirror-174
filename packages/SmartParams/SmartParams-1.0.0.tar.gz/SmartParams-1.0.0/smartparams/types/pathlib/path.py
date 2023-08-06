from pathlib import Path, PosixPath
from typing import Any

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return 'path' + self.missing_value


def simplifier(
    self: SmartRegister,
    default: Path,
    skip_default: bool,
    strict: bool,
) -> str:
    return str(default)


def from_str(
    self: SmartRegister,
    argument: str,
    subtypes: tuple[Any, ...],
) -> Path:
    return Path(argument)


def register() -> None:
    Smart.register(
        cls=Path,
        class_schema=class_schema,
        simplifier=simplifier,
        converter={
            str: from_str,
        },
    )

    Smart.register(
        cls=PosixPath,
        class_schema=class_schema,
        simplifier=simplifier,
    )

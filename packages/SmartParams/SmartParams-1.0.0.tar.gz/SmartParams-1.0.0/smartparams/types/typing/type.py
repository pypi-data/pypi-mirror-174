import inspect
from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Callable, Type, get_origin

from smartparams.register import SmartRegister
from smartparams.smart import Smart


def class_schema(
    self: SmartRegister,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> str:
    return self.class_path(subtypes[0]) if subtypes else 'type' + self.missing_value


def instance_schema(
    self: SmartRegister,
    instance: Any,
    subtypes: tuple[Any, ...],
    skip_default: bool,
) -> dict[str, Any]:
    if is_dataclass(instance):
        return _dataclass_schema(
            self=self,
            instance=instance,
            skip_default=skip_default,
        )

    return _instance_schema(
        self=self,
        instance=instance,
        skip_default=skip_default,
    )


def _instance_schema(
    self: SmartRegister,
    instance: Any,
    skip_default: bool,
) -> dict[str, Any]:
    try:
        signature = inspect.signature(instance)
    except ValueError:
        return {self.class_keyword: self.missing_value}

    maintype = get_origin(instance) or instance
    representation: dict[str, Any] = {
        self.class_keyword: (
            self.get_path(maintype) if self.has_class(maintype) else self.class_path(maintype)
        ),
    }

    for param in signature.parameters.values():
        if not (param.default is not param.empty and skip_default) and (
            param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
        ):
            representation[param.name] = self.schema(
                annotation=param.annotation,
                value=param.default,
                skip_default=skip_default,
            )

    return representation


def _dataclass_schema(
    self: SmartRegister,
    instance: Any,
    skip_default: bool,
) -> dict[str, Any]:
    representation: dict[str, Any] = {
        self.class_keyword: (
            self.get_path(instance) if self.has_class(instance) else self.class_path(instance)
        ),
    }

    for field in fields(instance):
        if not field.init:
            continue

        if field.default is not MISSING:
            representation[field.name] = self.schema(
                value=field.default,
                skip_default=skip_default,
            )
        elif field.default_factory is not MISSING:
            representation[field.name] = self.schema(
                value=field.default_factory(),
                skip_default=skip_default,
            )
        else:
            representation[field.name] = self.schema(
                annotation=field.type,
                skip_default=skip_default,
            )

    return representation


def simplifier(
    self: SmartRegister,
    default: type,
    skip_default: bool,
    strict: bool,
) -> str:
    return self.class_path(default)


def from_str(
    self: SmartRegister,
    argument: str,
    subtypes: tuple[Any, ...],
) -> Callable:
    smart_register = self.copy()
    smart_register(subtypes)
    return smart_register.import_class(argument)


def from_smart(
    self: SmartRegister,
    argument: Smart,
    subtypes: tuple[Any, ...],
) -> Callable:
    return argument.with_class(subtypes).cls


def register() -> None:
    for cls in (type, Type):
        Smart.register(
            cls=cls,
            class_schema=class_schema,
            instance_schema=instance_schema,
            simplifier=simplifier,
            converter={
                str: from_str,
                Smart: from_smart,
            },
        )

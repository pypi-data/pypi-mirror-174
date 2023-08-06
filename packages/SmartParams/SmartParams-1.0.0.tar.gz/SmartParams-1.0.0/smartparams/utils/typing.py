import inspect
from types import UnionType
from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

_T = TypeVar('_T')


def get_type_hints(parameters: Mapping[str, inspect.Parameter]) -> dict[str, Any]:
    type_hints: dict[str, Any] = {}
    for name, param in parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            param_type = param.annotation
        elif param.default is not inspect.Parameter.empty and param.default is not None:
            param_type = get_origin(param.default) or type(param.default)
        else:
            param_type = Any

        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_hints[name] = tuple[param_type, ...]  # type: ignore
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            type_hints[name] = dict[str, param_type]  # type: ignore
        else:
            type_hints[name] = param_type

    return type_hints


def get_return_type(cls: Callable[..., _T]) -> Type[_T]:
    if inspect.isclass(cls):
        return cls

    annotation = inspect.signature(cls).return_annotation
    return Any if annotation is inspect.Parameter.empty else annotation


def class_hierarchy(annotation: Any) -> Iterable[tuple[Any, tuple[Any, ...]]]:
    maintype = get_origin(annotation) or annotation
    subtypes = get_args(annotation)

    if maintype is None:
        yield type(None), tuple()
    elif maintype in (Union, UnionType):
        for subtype in subtypes:
            yield from class_hierarchy(subtype)
    else:
        yield maintype, subtypes
        if isinstance(maintype, type) and maintype is not type:
            for subclass in maintype.__subclasses__():
                yield from class_hierarchy(subclass)

import inspect
import itertools
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Hashable, overload

from typeguard import check_type

from smartparams.utils.imports import autodiscover, import_class
from smartparams.utils.loggers import Log
from smartparams.utils.typing import class_hierarchy, get_type_hints

_ClassSchema = Callable[['SmartRegister', tuple, bool], Any]
_InstanceSchema = Callable[['SmartRegister', Any, tuple, bool], Any]
_Simplifier = Callable[['SmartRegister', Any, bool, bool], Any]
_Smartifier = Callable[['SmartRegister', Any], Any]
_Mapper = Callable[[Any], Any]
_Converter = Callable[['SmartRegister', Any, Any], Any]
_Resolver = Callable[['SmartRegister', str, Any], Any]


@dataclass
class SmartObject:
    cls: Any
    path: str
    name: str
    class_schema: _ClassSchema | None
    instance_schema: _InstanceSchema | None
    simplifier: _Simplifier | None
    smartifier: _Smartifier | None
    mapper: dict[str, _Mapper]
    converter: dict[Any, _Converter]


class SmartRegister:
    class_keyword: str = 'class'
    missing_value: str = '???'

    def __init__(self) -> None:
        self.objects: dict[Any, SmartObject] = {}
        self.resolvers: list[_Resolver] = []

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{', '.join(obj.name for obj in self.objects.values())}]"

    @overload
    def __call__(
        self,
        classes: tuple[Any, ...],
        /,
    ) -> list[Any]:
        pass  # pragma: no cover

    @overload
    def __call__(
        self,
        *,
        name: str | None = None,
        class_schema: _ClassSchema | None = None,
        instance_schema: _InstanceSchema | None = None,
        simplifier: _Simplifier | None = None,
        smartifier: _Smartifier | None = None,
        mapper: dict[str, _Mapper] | None = None,
        converter: dict[Any, _Converter] | None = None,
    ) -> Callable[[Any], Any]:
        pass  # pragma: no cover

    @overload
    def __call__(
        self,
        cls: Any,
        *,
        name: str | None = None,
        class_schema: _ClassSchema | None = None,
        instance_schema: _InstanceSchema | None = None,
        simplifier: _Simplifier | None = None,
        smartifier: _Smartifier | None = None,
        mapper: dict[str, _Mapper] | None = None,
        converter: dict[Any, _Converter] | None = None,
    ) -> Any:
        pass  # pragma: no cover

    def __call__(
        self,
        cls: Any = None,
        *,
        name: str | None = None,
        class_schema: _ClassSchema | None = None,
        instance_schema: _InstanceSchema | None = None,
        simplifier: _Simplifier | None = None,
        smartifier: _Smartifier | None = None,
        mapper: dict[str, _Mapper] | None = None,
        converter: dict[Any, _Converter] | None = None,
    ) -> Any:
        if isinstance(cls, tuple):
            if not (
                name is None
                and class_schema is None
                and instance_schema is None
                and simplifier is None
                and smartifier is None
                and mapper is None
                and converter is None
            ):
                raise ValueError("cannot register annotations with keyword arguments")
            return self._register_annotations(cls)

        return self._register_class(
            cls=cls,
            name=name,
            class_schema=class_schema,
            instance_schema=instance_schema,
            simplifier=simplifier,
            smartifier=smartifier,
            mapper=mapper,
            converter=converter,
        )

    def copy(self) -> 'SmartRegister':
        return deepcopy(self)

    def clear(self) -> None:
        self.objects.clear()
        self.resolvers.clear()

    def has_class(
        self,
        cls: Any,
    ) -> bool:
        return isinstance(cls, Hashable) and cls in self.objects

    def has_name(
        self,
        name: str,
    ) -> bool:
        return any(name == obj.name for obj in self.objects.values())

    def has_path(
        self,
        path: str,
    ) -> bool:
        return any(path == obj.path for obj in self.objects.values())

    def has_class_schema(
        self,
        cls: Any,
    ) -> bool:
        return self.has_class(cls) and self.objects[cls].class_schema is not None

    def has_instance_schema(
        self,
        cls: Any,
    ) -> bool:
        return self.has_class(cls) and self.objects[cls].instance_schema is not None

    def has_simplifier(
        self,
        cls: Any,
    ) -> bool:
        return self.has_class(cls) and self.objects[cls].simplifier is not None

    def has_smartifier(
        self,
        cls: Any,
    ) -> bool:
        return self.has_class(cls) and self.objects[cls].smartifier is not None

    def has_mapper(
        self,
        cls: Any,
        mapper: str,
    ) -> bool:
        return self.has_class(cls) and mapper in self.objects[cls].mapper

    def has_converter(
        self,
        cls: Any,
        converter: Any,
    ) -> bool:
        return self.has_class(cls) and converter in self.objects[cls].converter

    def get_class_by_name(
        self,
        name: str,
    ) -> Any:
        for obj in self.objects.values():
            if obj.name == name:
                return obj.cls
        raise KeyError(name)

    def get_class_by_path(
        self,
        path: str,
    ) -> Any:
        for obj in self.objects.values():
            if obj.path == path:
                return obj.cls
        raise KeyError(path)

    def get_name(
        self,
        cls: Any,
    ) -> str:
        return self.objects[cls].name

    def get_path(
        self,
        cls: Any,
    ) -> str:
        return self.objects[cls].path

    def get_class_schema(
        self,
        cls: Any,
    ) -> _ClassSchema:
        if (class_schema := self.objects[cls].class_schema) is None:
            raise ValueError(f"{cls} has not class schema")
        return class_schema

    def get_instance_schema(
        self,
        cls: Any,
    ) -> _InstanceSchema:
        if (instance_schema := self.objects[cls].instance_schema) is None:
            raise ValueError(f"{cls} has not instance schema")
        return instance_schema

    def get_simplifier(
        self,
        cls: Any,
    ) -> _Simplifier:
        if (simplifier := self.objects[cls].simplifier) is None:
            raise ValueError(f"{cls} has not simplifier")
        return simplifier

    def get_smartifier(
        self,
        cls: Any,
    ) -> _Smartifier:
        if (smartifier := self.objects[cls].smartifier) is None:
            raise ValueError(f"{cls} has not smartifier")
        return smartifier

    def get_mapper(
        self,
        cls: Any,
        mapper: str,
    ) -> _Mapper:
        return self.objects[cls].mapper[mapper]

    def get_converter(
        self,
        cls: Any,
        converter: Any,
    ) -> _Converter:
        return self.objects[cls].converter[converter]

    @staticmethod
    def class_name(cls: Any) -> str:
        if not hasattr(cls, '__qualname__'):
            raise ValueError(f"cannot determined name of {cls}")
        return cls.__qualname__

    @staticmethod
    def class_path(cls: Any) -> str:
        if callable(cls) and hasattr(cls, '__module__') and hasattr(cls, '__qualname__'):
            if cls.__module__ == 'builtins':
                return cls.__qualname__
            return cls.__module__ + '.' + cls.__qualname__

        raise ValueError(f"cannot determine path of {cls}")

    def import_class(
        self,
        name: str,
    ) -> Callable:
        """Returns class if registered, imports it otherwise.

        Args:
            name: Class name to be imported.

        Returns:
            Class.

        """
        if self.has_name(name):
            Log.import_.debug("importing registered class by name: %s", name)
            return self.get_class_by_name(name)

        if self.has_path(name):
            Log.import_.debug("importing registered class by path: %s", name)
            return self.get_class_by_path(name)

        Log.import_.warning("importing unregistered class: %s", name)
        return import_class(name)

    @staticmethod
    def autodiscover(
        path: str | Path = '.',
        include: str = '',
        exclude: str = '',
    ) -> list[Path]:
        msg = "auto-discovering python modules in '%s', including: '%s', excluding: '%s'"
        Log.import_.info(msg, path, include, exclude)
        return autodiscover(
            path=Path(path),
            include=include,
            exclude=exclude,
        )

    def instantiate(
        self,
        cls: Callable,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        """Instantiates class.

        Args:
            cls: Class to be instantiated.
            args: Positional arguments to be passed to class.
            kwargs: Keyword arguments to be passed to class.

        Returns:
            Class instance.

        """
        path = self.class_path(cls)
        _args = '; '.join(str(args).splitlines())
        _kwargs = '; '.join(str(kwargs).splitlines())
        Log.init.debug("starting instantiate '%s' with args=%s and kwargs=%s", path, _args, _kwargs)

        try:
            signature = inspect.signature(cls)
        except ValueError:
            Log.init.debug("cannot get signature of '%s'", path)
            Log.init.debug("instantiating '%s' with args=%s and kwargs=%s", path, _args, _kwargs)
            instance = cls(*args, **kwargs)
            Log.init.debug("'%s' has been instantiated", path)
            return instance

        try:
            arguments = signature.bind(*args, **kwargs).arguments
        except TypeError as exc:
            raise TypeError(f"cannot instantiate '{path}'; {'; '.join(exc.args)}")

        num_pos_args = len(args)
        pos_args = []
        kw_args = {}

        for pos, (name, expected_type) in enumerate(get_type_hints(signature.parameters).items()):
            if name not in arguments:
                continue

            argument = arguments[name]

            for resolver in self.resolvers:
                argument = resolver(self, name, argument)

            if self.has_mapper(cls, name):
                try:
                    Log.init.debug("mapping argument '%s'", name)
                    argument = self.objects[cls].mapper[name](argument)
                except Exception as exc:
                    Log.init.error("cannot map argument '%s' - %s", name, exc)
                    raise exc
            else:
                try:
                    Log.init.debug("converting argument '%s'", name)
                    argument = self.convert(
                        argument=argument,
                        expected_type=expected_type,
                    )
                except Exception as exc:
                    Log.init.error("cannot convert argument '%s' - %s", name, exc)
                    raise exc

            match signature.parameters[name].kind:
                case inspect.Parameter.VAR_POSITIONAL:
                    pos_args.extend(argument)
                case inspect.Parameter.VAR_KEYWORD:
                    kw_args.update(argument)
                case _:
                    if pos < num_pos_args:
                        pos_args.append(argument)
                    else:
                        kw_args[name] = argument

            try:
                check_type(
                    argname=f"'{name}'",
                    value=argument,
                    expected_type=expected_type,
                )
            except TypeError as exc:
                Log.init.error("; ".join(exc.args))

        _args = '; '.join(str(tuple(pos_args)).splitlines())
        _kwargs = '; '.join(str(kw_args).splitlines())
        Log.init.debug("instantiating '%s' with args=%s and kwargs=%s", path, _args, _kwargs)
        instance = cls(*pos_args, **kw_args)
        Log.init.debug("'%s' has been instantiated", path)
        return instance

    def convert(
        self,
        argument: Any,
        expected_type: Any = Any,
    ) -> Any:
        """Map argument to expected_type type.

        Args:
            argument: Argument to be mapped.
            expected_type: Expected type of argument.

        Returns:
            Mapped argument.

        """
        argument_type = type(argument)
        converters = []

        for maintype, subtypes in itertools.chain(
            class_hierarchy(expected_type),
            ((Any, (expected_type,)),),
        ):
            if argument_type == maintype:
                if self.has_converter(maintype, argument_type):
                    Log.init.debug("converting type %s", argument_type)
                    return self.get_converter(maintype, argument_type)(self, argument, subtypes)

                return argument

            if self.has_converter(maintype, argument_type):
                converters.append((maintype, subtypes))

        if converters:
            (maintype, subtypes), *rest = converters
            if rest:
                Log.init.debug("there are many possible type converters from %s", argument_type)

            Log.init.debug(
                "converting type from %s to %s%s", argument_type, maintype, list(subtypes)
            )
            return self.get_converter(maintype, argument_type)(self, argument, subtypes)

        Log.init.debug("missing type converter from %s to %s", argument_type, expected_type)
        return argument

    def smartify(
        self,
        obj: Any,
    ) -> Any:
        if self.has_smartifier(obj_type := type(obj)):
            return self.get_smartifier(obj_type)(self, obj)
        return obj

    def simplify(
        self,
        obj: Any,
        skip_default: bool = True,
        strict: bool = True,
    ) -> Any:
        if self.has_class(obj):
            return self.get_path(obj)

        if self.has_simplifier(obj_type := type(obj)):
            return self.get_simplifier(obj_type)(self, obj, skip_default, strict)

        if strict:
            raise TypeError(f"cannot simplify '{obj}' object, register simplifier for {obj_type}")

        return self.missing_value

    def schema(
        self,
        annotation: Any = inspect.Parameter.empty,
        value: Any = inspect.Parameter.empty,
        skip_default: bool = False,
    ) -> Any:
        if value is not inspect.Parameter.empty:
            if self.has_class(value):
                return self.get_path(value)

            if self.has_simplifier(value_type := type(value)):
                return self.get_simplifier(value_type)(self, value, skip_default, False)

        if annotation is not inspect.Parameter.empty:
            converters = []
            for maintype, subtypes in class_hierarchy(annotation):
                if self.has_class_schema(maintype):
                    return self.get_class_schema(maintype)(self, subtypes, skip_default)

                converters.append((maintype, subtypes))

            for maintype, subtypes in converters:
                if self.has_instance_schema(cls := type(maintype)):
                    return self.get_instance_schema(cls)(self, maintype, subtypes, skip_default)

        return self.missing_value

    def _register_class(
        self,
        cls: Any = None,
        *,
        name: str | None = None,
        class_schema: _ClassSchema | None = None,
        instance_schema: _InstanceSchema | None = None,
        simplifier: _Simplifier | None = None,
        smartifier: _Smartifier | None = None,
        mapper: dict[str, _Mapper] | None = None,
        converter: dict[Any, _Converter] | None = None,
    ) -> Any:
        def smart_register(cls_: Any) -> Any:
            nonlocal name

            if self.has_class(cls_):
                obj = self.objects[cls_]

                if name is not None and obj.name != name:
                    if self.has_name(name):
                        raise ValueError(f"cannot rename '{obj.path}', name '{name}' already exist")

                    Log.register.warning("rename '%s' from '%s' to '%s'", obj.path, obj.name, name)
                    obj.name = name

                if class_schema is not None and obj.class_schema != class_schema:
                    Log.register.warning("'%s' class schema has been overridden", obj.path)
                    obj.class_schema = class_schema

                if instance_schema is not None and obj.instance_schema != instance_schema:
                    Log.register.warning("'%s' instance schema has been overridden", obj.path)
                    obj.instance_schema = instance_schema

                if simplifier is not None and obj.simplifier != simplifier:
                    Log.register.warning("'%s' simplifier has been overridden", obj.path)
                    obj.simplifier = simplifier

                if smartifier is not None and obj.smartifier != smartifier:
                    Log.register.warning("'%s' smartifier has been overridden", obj.path)
                    obj.smartifier = smartifier

                if mapper is not None:
                    for mapper_key, mapper_function in mapper.items():
                        if mapper_key in obj.mapper:
                            if obj.mapper[mapper_key] != mapper_function:
                                msg = "mapper argument '%s' of '%s' has been overridden"
                                Log.register.warning(msg, mapper_key, obj.path)
                                obj.mapper[mapper_key] = mapper_function
                        else:
                            obj.mapper[mapper_key] = mapper_function

                if converter is not None:
                    for converter_key, converter_function in converter.items():
                        if converter_key in obj.converter:
                            if obj.converter[converter_key] != converter_function:
                                msg = "converter from %s to %s has been overridden"
                                Log.register.warning(msg, converter_key, cls_)
                                obj.converter[converter_key] = converter_function
                        else:
                            obj.converter[converter_key] = converter_function

            else:
                if name is None:
                    name = self.class_name(cls_)

                path = self.class_path(cls_)
                if self.has_name(name):
                    raise ValueError(f"cannot register '{path}', name '{name}' already exist")

                Log.register.debug("registering '%s' with name '%s'", path, name)

                self.objects[cls_] = SmartObject(
                    cls=cls_,
                    path=path,
                    name=name,
                    class_schema=class_schema,
                    instance_schema=instance_schema,
                    simplifier=simplifier,
                    smartifier=smartifier,
                    mapper=mapper or {},
                    converter=converter or {},
                )

            return cls_

        if cls is None:
            return smart_register

        smart_register(cls)
        return cls

    def _register_annotations(
        self,
        classes: tuple[Any, ...],
    ) -> list[Any]:
        registered = []
        for cls in classes:
            for maintype, subtype in class_hierarchy(cls):
                path = self.class_path(maintype)
                if self.has_class(maintype):
                    Log.register.debug("skipping '%s', already registered", path)
                    continue

                name = self.class_name(maintype)
                if self.has_name(name):
                    Log.register.debug("skipping '%s', name '%s' already exist", path, name)
                    continue

                self(
                    cls=maintype,
                    name=name,
                )
                registered.append(maintype)

        return registered

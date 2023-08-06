import copy
import itertools
import sys
from datetime import timezone
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generic,
    ItemsView,
    Iterable,
    KeysView,
    Mapping,
    Type,
    TypeVar,
    ValuesView,
    overload,
)

from smartparams.io import json, yaml
from smartparams.register import SmartRegister
from smartparams.utils import directory, parser
from smartparams.utils.default import Default
from smartparams.utils.loggers import Log
from smartparams.utils.typing import get_return_type

_T = TypeVar('_T')
_KEY_SEPARATOR = '.'


class Smart(dict[str, Any], Generic[_T]):
    """Creates a wrapper for a class or function that can be configurable from a file or a cli.

    Smart class has functionality of both partial and dict classes. It allows creating
    objects with lazy instantiating. This makes possible injecting values from config
    file or command line.

    Attributes:
        register: Global instance of SmartRegister. Store classes and functions available
            for all Smart instances.

    Args:
        cls: Callable object to be wrapped.
        **params: Partial keyword arguments to be passed to the callable object.

    """

    register = SmartRegister()

    @overload
    def __init__(self, /, **params: Any) -> None:
        pass  # pragma: no cover

    @overload
    def __init__(self, cls: Callable[..., _T], /, **params: Any) -> None:
        pass  # pragma: no cover

    @overload
    def __init__(self, cls: str, /, **params: Any) -> None:
        pass  # pragma: no cover

    @overload
    def __init__(self, cls: Mapping[str, Any], /, **params: Any) -> None:
        pass  # pragma: no cover

    @overload
    def __init__(self, cls: Iterable[tuple[str, Any] | str], /, **params: Any) -> None:
        pass  # pragma: no cover

    def __init__(
        self,
        cls: (
            Callable[..., _T] | str | Mapping[str, Any] | Iterable[tuple[str, Any] | str] | None
        ) = None,
        /,
        **params: Any,
    ) -> None:
        super().__init__()
        self.register = self.register.copy()

        if callable(cls) or isinstance(cls, str):
            if self.register.class_keyword in params:
                raise ValueError(
                    f"cannot pass `cls` and keyword `{self.register.class_keyword}` together"
                )
            self[self.register.class_keyword] = cls
        elif cls is not None:
            self.update(cls)

        self.update(params)

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _T:
        """Creates instance of given class.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An class instance.

        """
        cls = self.cls
        params = self.params

        if common := set(params).intersection(kwargs):
            Log.init.warning("following params have been overridden: %s", cls, common)

        params.update(kwargs)

        return self.register.instantiate(
            cls=cls,
            args=args,
            kwargs=dict(params),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __getattr__(
        self,
        item: str,
    ) -> Any:
        if not item.startswith('_'):
            return self[item]
        raise AttributeError(item)

    def __setattr__(
        self,
        key: str,
        value: Any,
    ) -> None:
        if key.startswith('_') or key in self.__dir__():
            super().__setattr__(key, value)
        else:
            self[key] = value

    @overload
    def __getitem__(self, key: str) -> Any:
        pass  # pragma: no cover

    @overload
    def __getitem__(self, key: Callable[..., _T]) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def __getitem__(self, key: tuple[Callable[..., _T], ...]) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def __getitem__(self, key: tuple[Any, ...]) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def __getitem__(self, key: Any) -> 'Smart[_T]':
        pass  # pragma: no cover

    def __getitem__(
        self,
        key: Any,
    ) -> Any:
        if isinstance(key, str):
            try:
                return self._getitem(key)
            except KeyError as exc:
                raise KeyError(key) from exc

        return self.with_class(key)

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        self._setitem(key, value)

    def __delitem__(
        self,
        key: str,
    ) -> None:
        try:
            self._delitem(key)
        except KeyError as exc:
            raise KeyError(key) from exc

    def __contains__(
        self,
        key: Any,
    ) -> bool:
        return isinstance(key, str) and self._contains(key)

    @property
    def params(self) -> 'Smart':
        """Returns the parameters that will be provided when creating an instance of the class."""
        params = self.copy()
        params.pop(self.register.class_keyword, None)
        return params

    @property
    def type(self) -> Type[_T]:
        """Returns class or function's return type."""
        return get_return_type(self.cls)

    @property
    def cls(self) -> Callable[..., _T]:
        """Returns class or function and, if necessary, imports it."""
        cls = self[self.register.class_keyword]

        if callable(cls):
            return cls

        if isinstance(cls, str):
            return self.register.import_class(cls)

        raise TypeError(f"key `{self.register.class_keyword}` is not callable")

    @cls.setter
    def cls(
        self,
        cls: Callable | str,
    ) -> None:
        """Sets new class."""
        if not (isinstance(cls, str) or callable(cls)):
            raise TypeError("`cls` have to be callable, str or None")
        self[self.register.class_keyword] = cls

    @cls.deleter
    def cls(self) -> None:
        """Deletes class."""
        del self[self.register.class_keyword]

    @overload
    def with_class(self, cls: Callable[..., _T], /) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def with_class(self, cls: tuple[Callable[..., _T]], /) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def with_class(self, cls: tuple[Any, ...], /) -> 'Smart[_T]':
        pass  # pragma: no cover

    @overload
    def with_class(self, cls: Any, /) -> 'Smart[_T]':
        pass  # pragma: no cover

    def with_class(
        self,
        cls: Any,
        /,
    ) -> 'Smart[_T]':
        smart: Smart = self.copy()
        if classes := cls if isinstance(cls, tuple) else (cls,):
            first_class, *_ = classes
            if callable(first_class) and smart.register.class_keyword not in smart:
                smart.cls = first_class
            smart.register(classes)
        return smart

    def keys(  # type: ignore
        self,
        flatten: bool = False,
    ) -> KeysView[str]:
        """Returns keys existing in the dictionary.

        Args:
            flatten: Whether to return the flattened keys in the nested dictionaries.

        Returns:
            Keys from dictionary.

        """
        if flatten:
            return dict(self._flatten()).keys()
        return super().keys()

    def values(  # type: ignore
        self,
        flatten: bool = False,
    ) -> ValuesView[Any]:
        """Returns values existing in the dictionary.

        Args:
            flatten: Whether to return the flattened values in the nested dictionaries.

        Returns:
            Values from dictionary.

        """
        if flatten:
            return dict(self._flatten()).values()
        return super().values()

    def items(  # type: ignore
        self,
        flatten: bool = False,
    ) -> ItemsView[str, Any]:
        """Returns items existing in the dictionary.

        Args:
            flatten: Whether to return the flattened items in the nested dictionaries.

        Returns:
            Items from dictionary.

        """
        if flatten:
            return dict(self._flatten()).items()
        return super().items()

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Returns value of given key from dictionary.

        Args:
            key: The key of value.
            default: Value returned if key doesn't exist.

        Returns:
            Value matched with given key.

        """
        return self._get(key, default)

    @overload
    def pop(self, key: str) -> Any:
        pass  # pragma: no cover

    @overload
    def pop(self, key: str, default: Any = ...) -> Any:
        pass  # pragma: no cover

    def pop(
        self,
        key: str,
        default: Any = Default,
    ) -> Any:
        """Removes and returns value of given key from dictionary.

        Args:
            key: The key of value.
            default: Value returned if key doesn't exist.

        Returns:
            Removed value.

        Raises:
            KeyError if key doesn't exist and default value not specified.

        """
        try:
            return self._pop(key, default)
        except KeyError as exc:
            raise KeyError(key) from exc

    def update(  # type: ignore
        self,
        iterable: Mapping[str, Any] | Iterable[tuple[str, Any] | str] | None = None,
        /,
        **kwargs: Any,
    ) -> None:
        """Updates existing items with given data or keyword arguments.

        Args:
            iterable: Mapping or iterable with items to update.
            **kwargs: New items to update.

        """
        if isinstance(iterable, Mapping):
            for k, v in iterable.items():
                self[k] = v
        elif isinstance(iterable, Iterable) and not isinstance(iterable, str):
            for item in iterable:
                k, v = parser.parse_param(item) if isinstance(item, str) else item
                self[k] = v
        elif iterable is not None:
            raise TypeError(f"`iterable` must be mapping or iterable, not {type(iterable)}")

        for k, v in kwargs.items():
            self[k] = v

    @classmethod
    def merge(
        cls,
        *smarts: 'Smart',
    ) -> 'Smart':
        """Merges given smart dictionaries.

        Args:
            *smarts: Smart instances to be merged.

        Returns:
            Smart instance with merged dictionaries.

        """
        merged: Smart = cls()
        for smart in smarts:
            for key, value in smart.copy()._flatten():
                is_key_in_merged = key in merged
                if is_key_in_merged and isinstance(merged[key], list) and isinstance(value, list):
                    merged[key].extend(value)
                else:
                    if is_key_in_merged:
                        Log.merge.warning("key '%s' has been overridden", key)
                    merged[key] = value
        return merged

    def copy(self) -> 'Smart[_T]':
        """Returns current smart object deep copy."""
        return copy.deepcopy(self)

    def explode(
        self,
        *keys: str,
    ) -> Iterable['Smart[_T]']:
        """Explodes the values in the lists of given keys.

        Args:
            *keys: Keys to be exploded.

        Yields:
            Generates Smart instances with every combination of exploded sequences.

        """
        dictionary = {key: self[key] for key in keys}

        if not all(isinstance(value, list | tuple | set) for value in dictionary.values()):
            raise TypeError("all values to explode have to be list, tuple or set")

        for values in itertools.product(*dictionary.values()):
            exploded = self.copy()
            for key, value in zip(dictionary.keys(), values):
                exploded[key] = value
            yield exploded

    def schema(
        self,
        skip_default: bool = False,
    ) -> 'Smart':
        """Returns class of function representation based on python type annotation.

        Args:
            skip_default: Whether skip arguments with default values.

        Returns:
            Smart dictionary with representation of class or function.

        """
        schema = self.register.schema(
            annotation=self.cls,
            skip_default=skip_default,
        )
        return self.__class__(schema)

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> 'Smart':
        """Loads smart object from given path.

        Args:
            path: Path to the file.

        Returns:
            Smart instance with loaded items.

        """
        path = Path(path)
        match path.suffix.lower():
            case '.yaml' | '.yml':
                data = yaml.load(
                    path=path,
                )
            case '.json':
                data = json.load(
                    path=path,
                )
            case suffix:
                raise ValueError(f"file {suffix} is not supported, use .yaml or .json instead")

        if not isinstance(data, dict):
            raise ValueError("file should contain a dictionary")

        Log.io.info("params have been loaded from '%s'", path)
        return cls(**data)

    @classmethod
    def from_cli(cls) -> 'Smart':
        """Creates smart object from cli arguments."""
        Log.io.info("loading cli params: %s", " ".join(params := sys.argv[1:]))
        return cls(params)

    def save(
        self,
        path: str | Path,
    ) -> None:
        """Saves dict representation to given path.

        Args:
            path: Path to save the dictionary.

        """
        path = Path(path)

        match path.suffix.lower():
            case '.yaml' | '.yml':
                yaml.save(
                    data=self.to_dict(),
                    path=path,
                )
            case '.json':
                json.save(
                    data=self.to_dict(),
                    path=path,
                )
            case suffix:
                raise ValueError(f"file {suffix} is not supported, use .yaml or .json instead")

        Log.io.info("params have been saved to '%s'", path)

    def to_dict(self) -> dict:
        """Returns dict representation of current object."""
        return self.register.simplify(self)

    def to_yaml(self) -> str:
        """Returns yaml representation of current object."""
        return yaml.to_string(self.to_dict())

    def to_json(self) -> str:
        """Returns json representation of current object."""
        return json.to_string(self.to_dict())

    @staticmethod
    def mkdir(
        path: str | Path,
        version: str | None = None,
        tz: timezone | None = None,
    ) -> Path:
        """Creates directory with unique version.

        Args:
            path: Path to directory to be created.
            version: Pattern for new folder name. Available fields: num, hash, h4, h6, h8, uuid,
                adj, noun, animal, Y, m, d, H, M, S, f.
            tz: Timezone for datatime class.

        Returns:
            Path to newly created directory.

        """
        dir_path = directory.mkdir(
            path=Path(path),
            version=version,
            tz=tz,
        )
        Log.io.info("directory '%s' has been created", dir_path)
        return dir_path

    def _getitem(
        self,
        key: str,
    ) -> Any:
        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        obj = super().__getitem__(key)
        if separator:
            if isinstance(obj, self.__class__):
                return obj._getitem(subkey)
            raise KeyError(subkey)
        return obj

    def _setitem(
        self,
        key: str,
        value: Any,
    ) -> None:
        if not isinstance(key, str):
            raise TypeError(f"key `{key}` have to be str")

        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        if separator:
            obj = super().get(key)
            if not isinstance(obj, self.__class__):
                obj = self.__class__()
                super().__setitem__(key, obj)
            obj._setitem(subkey, value)
        else:
            super().__setitem__(key, self.register.smartify(value))

    def _delitem(
        self,
        key: str,
    ) -> None:
        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        if separator:
            obj = super().get(key)
            if isinstance(obj, self.__class__):
                obj._delitem(subkey)
            else:
                raise KeyError(subkey)
        else:
            super().__delitem__(key)

    def _contains(
        self,
        key: str,
    ) -> bool:
        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        isin = super().__contains__(key)
        if separator:
            obj = super().get(key)
            return isin and isinstance(obj, self.__class__) and obj._contains(subkey)
        return isin

    def _get(
        self,
        key: str,
        default: Any,
    ) -> Any:
        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        obj = super().get(key, default)
        if separator:
            if isinstance(obj, self.__class__):
                return obj._get(subkey, default)
            return default
        return obj

    def _pop(
        self,
        key: str,
        default: Any = Default,
    ) -> Any:
        key, separator, subkey = key.partition(_KEY_SEPARATOR)
        if separator:
            obj = super().get(key)
            if isinstance(obj, self.__class__):
                return obj._pop(subkey, default)
            if default is Default:
                raise KeyError(subkey)
            return default
        if default is Default:
            return super().pop(key)
        return super().pop(key, default)

    def _flatten(self) -> list[tuple[str, Any]]:
        flatten_items: list[tuple[str, Any]] = []
        for key, value in super().items():
            if isinstance(value, self.__class__) and (items := value._flatten()):
                flatten_items.extend(((key + _KEY_SEPARATOR + sk, sv) for sk, sv in items))
            else:
                flatten_items.append((key, value))
        return flatten_items

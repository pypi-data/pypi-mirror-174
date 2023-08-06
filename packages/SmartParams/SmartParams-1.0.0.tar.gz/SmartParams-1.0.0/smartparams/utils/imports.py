import importlib
import re
from pathlib import Path
from typing import Callable

from smartparams.utils.loggers import Log


def import_class(name: str) -> Callable:
    *obj_path, obj_name = name.split('.')

    for i in range(len(obj_path), 0, -1):
        try:
            module = importlib.import_module('.'.join(obj_path[:i]))
        except ModuleNotFoundError:
            pass
        else:
            try:
                for j in range(len(obj_path) - i):
                    module = getattr(module, obj_path[i + j])
                obj = getattr(module, obj_name)
            except (ValueError, AttributeError):
                break
            else:
                if not callable(obj):
                    raise ImportError(f"cannot import '{name}' class")
                return obj

    raise ImportError(f"cannot import '{name}' class")


def autodiscover(
    path: Path,
    include: str = '',
    exclude: str = '',
) -> list[Path]:
    if include and exclude:
        raise ValueError("cannot use `include` and `exclude` together")

    paths = []

    for module_path in (path,) if path.is_file() and path.suffix == '.py' else path.rglob('*.py'):
        module_path = module_path.relative_to(path)

        if include and not re.search(include, str(module_path)):
            continue

        if exclude and re.search(exclude, str(module_path)):
            continue

        module = '.'.join(module_path.with_suffix('').parts)
        try:
            Log.import_.debug("importing '%s' module", module)
            importlib.import_module(module)
        except Exception as exc:
            error_type = type(exc).__qualname__
            Log.import_.warning("cannot import '%s' module due to %s(%s)", module, error_type, exc)
        else:
            paths.append(module_path)

    return paths

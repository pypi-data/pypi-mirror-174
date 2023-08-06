from pathlib import Path
from typing import Any

import yaml


def load(path: Path) -> Any:
    with path.open() as stream:
        return yaml.safe_load(stream)


def save(
    data: Any,
    path: Path,
) -> Any:
    with path.open('w') as stream:
        yaml.safe_dump(
            data=data,
            stream=stream,
            sort_keys=False,
            allow_unicode=True,
        )


def to_string(data: Any) -> str:
    return yaml.safe_dump(
        data=data,
        sort_keys=False,
        allow_unicode=True,
    )

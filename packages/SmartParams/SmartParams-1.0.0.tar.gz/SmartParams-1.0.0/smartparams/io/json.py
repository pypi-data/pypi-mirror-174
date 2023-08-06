import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    with path.open() as stream:
        return json.load(stream)


def save(
    data: Any,
    path: Path,
) -> Any:
    with path.open('w') as stream:
        json.dump(
            obj=data,
            fp=stream,
            indent=2,
            sort_keys=False,
            ensure_ascii=False,
            default=str,
        )


def to_string(data: Any) -> str:
    return json.dumps(
        obj=data,
        indent=2,
        sort_keys=False,
        ensure_ascii=False,
        default=str,
    )

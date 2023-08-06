import json
from typing import Any

_PARAM_SEPARATOR = '='


def parse_param(param: str) -> tuple[str, Any]:
    key, separator, raw_value = param.partition(_PARAM_SEPARATOR)

    if not separator:
        raise ValueError(f"parameter `{key}` has not assigned value")

    try:
        value = json.loads(raw_value)
    except json.decoder.JSONDecodeError:
        value = raw_value

    return key, value

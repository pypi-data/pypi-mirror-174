from typing import Any

from smartparams import SmartRegister
from smartparams.utils.loggers import Log


def missing_value_resolver(
    self: SmartRegister,
    name: str,
    argument: Any,
) -> Any:
    if isinstance(argument, str) and argument.endswith(self.missing_value):
        Log.init.warning("argument '%s' has missing value", name)
    return argument

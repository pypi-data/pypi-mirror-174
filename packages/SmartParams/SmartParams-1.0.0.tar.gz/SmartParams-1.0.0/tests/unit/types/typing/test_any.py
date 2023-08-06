from typing import Any

from smartparams import Smart
from smartparams.types.typing.any import class_schema, from_smart
from tests.commons.classes import some_function
from tests.unit.types import Types


class TestAny(Types.Test):
    CLS = Any
    CONVERT_VALUES = {
        Smart: Smart(some_function),
    }

    def init_register(self) -> None:
        self.register(
            cls=Any,
            class_schema=class_schema,
            converter={
                Smart: from_smart,
            },
        )

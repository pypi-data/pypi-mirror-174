from typing import Callable

from smartparams import Smart
from smartparams.types.typing.callable import (
    class_schema,
    from_smart,
    from_str,
    simplifier,
)
from tests.commons.classes import some_function
from tests.unit.types import Types


class TestCallable(Types.Test):
    CLS = Callable
    DEFAULT = some_function
    CONVERT_VALUES = {
        Smart: Smart(some_function),
        str: 'Callable',
    }

    def init_register(self) -> None:
        self.register(
            cls=Callable,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                Smart: from_smart,
                str: from_str,
            },
        )

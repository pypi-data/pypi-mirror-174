from typing import Any

from smartparams import Smart
from smartparams.types.builtins.dict import (
    class_schema,
    from_dict,
    from_smart,
    simplifier,
)
from tests.unit.types import Types


class TestDict(Types.Test):
    CLS = dict
    DEFAULT = dict(a='x', b=5, c=False)
    CONVERT_VALUES: dict[Any, Any] = {
        dict: dict(a='x', b=5, c=False),
        Smart: Smart(a='x', b=5, c=False),
    }
    SUBTYPES = (Any, Any)

    def init_register(self) -> None:
        self.register(
            cls=dict,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                Smart: from_smart,
                dict: from_dict,
            },
        )

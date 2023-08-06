from smartparams import Smart
from smartparams.types.smartparams.smart import (
    class_schema,
    from_smart,
    from_str,
    simplifier,
)
from tests.commons.classes import some_function
from tests.unit.types import Types


class TestSmart(Types.Test):
    CLS = Smart
    DEFAULT: Smart = Smart()
    CONVERT_VALUES = {
        Smart: Smart(some_function),
        str: 'Smart',
    }

    def init_register(self) -> None:
        self.register(
            cls=Smart,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                Smart: from_smart,
                str: from_str,
            },
        )

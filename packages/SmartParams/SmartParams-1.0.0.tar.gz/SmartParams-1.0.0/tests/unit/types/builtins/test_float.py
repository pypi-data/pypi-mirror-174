from smartparams.types.builtins.float import class_schema, simplifier
from tests.unit.types import Types


class TestFloat(Types.Test):
    CLS = float
    DEFAULT = 1.5

    def init_register(self) -> None:
        self.register(
            cls=float,
            class_schema=class_schema,
            simplifier=simplifier,
        )

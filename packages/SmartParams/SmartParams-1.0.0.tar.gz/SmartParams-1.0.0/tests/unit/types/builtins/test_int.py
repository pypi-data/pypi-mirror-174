from smartparams.types.builtins.int import class_schema, simplifier
from tests.unit.types import Types


class TestInt(Types.Test):
    CLS = int
    DEFAULT = 5

    def init_register(self) -> None:
        self.register(
            cls=int,
            class_schema=class_schema,
            simplifier=simplifier,
        )

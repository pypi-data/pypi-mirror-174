from smartparams.types.builtins.none import class_schema, simplifier
from tests.unit.types import Types


class TestNoneType(Types.Test):
    CLS = type(None)
    DEFAULT = None

    def init_register(self) -> None:
        self.register(
            cls=type(None),
            class_schema=class_schema,
            simplifier=simplifier,
        )

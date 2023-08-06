from smartparams.types.builtins.bool import class_schema, simplifier
from tests.unit.types import Types


class TestBool(Types.Test):
    CLS = bool
    DEFAULT = True

    def init_register(self) -> None:
        self.register(
            cls=bool,
            class_schema=class_schema,
            simplifier=simplifier,
        )

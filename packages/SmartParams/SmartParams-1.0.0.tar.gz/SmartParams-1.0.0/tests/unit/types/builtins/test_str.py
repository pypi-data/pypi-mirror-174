from smartparams.types.builtins.str import class_schema, instance_schema, simplifier
from tests.unit.types import Types


class TestStr(Types.Test):
    CLS = str
    DEFAULT = 'x'

    def init_register(self) -> None:
        self.register(
            cls=str,
            class_schema=class_schema,
            instance_schema=instance_schema,
            simplifier=simplifier,
        )

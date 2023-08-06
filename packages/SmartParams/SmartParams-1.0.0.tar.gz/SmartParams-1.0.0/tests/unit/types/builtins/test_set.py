from smartparams.types.builtins.set import class_schema, from_list, simplifier
from tests.unit.types import Types


class TestSet(Types.Test):
    CLS = set
    DEFAULT = {'x', 5, False}
    CONVERT_VALUES = {
        list: ['x', 5, False],
    }

    def init_register(self) -> None:
        self.register(
            cls=set,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                list: from_list,
            },
        )

from smartparams.types.builtins.list import class_schema, from_list, simplifier
from tests.unit.types import Types


class TestList(Types.Test):
    CLS = list
    DEFAULT = ['x', 5, False]
    CONVERT_VALUES = {
        list: ['x', 5, False],
    }

    def init_register(self) -> None:
        self.register(
            cls=list,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                list: from_list,
            },
        )

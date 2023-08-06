from typing import ForwardRef

from smartparams.types.typing.forwardref import instance_schema
from tests.unit.types import Types


class TestForwardRef(Types.Test):
    CLS = ForwardRef
    DEFAULT = ForwardRef('A')

    def init_register(self) -> None:
        self.register(
            cls=ForwardRef,
            instance_schema=instance_schema,
        )

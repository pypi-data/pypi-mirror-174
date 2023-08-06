from typing import Any
from unittest.mock import Mock, call

from smartparams.types.builtins.tuple import class_schema, from_list, simplifier
from tests.unit.types import Types


class TestTuple(Types.Test):
    CLS = tuple
    DEFAULT = ('x', 5, False)
    CONVERT_VALUES = {
        list: ['x', 5, False],
    }

    def init_register(self) -> None:
        self.register(
            cls=tuple,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                list: from_list,
            },
        )

    def test_from_list__register__fill_any(self) -> None:
        subtypes = (Mock(), Mock())
        register = Mock()
        list_values = [Mock(), Mock(), Mock(), Mock(), Mock()]

        from_list(register, list_values, subtypes)

        register.convert.assert_has_calls(
            [call(value, subtype) for value, subtype in zip(list_values, subtypes + (Any,) * 3)],
        )

    def test_from_list__register__homogenous_types(self) -> None:
        subtypes = (Mock(), Mock(), ...)
        register = Mock()
        list_values = [Mock(), Mock(), Mock(), Mock(), Mock()]

        from_list(register, list_values, subtypes)

        register.convert.assert_has_calls(
            [call(value, subtype) for value, subtype in zip(list_values, (subtypes[0],) * 5)],
        )

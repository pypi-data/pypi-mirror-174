from dataclasses import field, make_dataclass

from smartparams import Smart
from smartparams.types.typing.type import (
    class_schema,
    from_smart,
    from_str,
    instance_schema,
    simplifier,
)
from tests.commons.classes import ParentA, ParentC
from tests.unit.types import Types


class TestType(Types.Test):
    CLS = type
    DEFAULT = ParentA
    CONVERT_VALUES = {
        Smart: Smart(ParentA),
        str: 'type',
    }

    def init_register(self) -> None:
        self.register(
            cls=type,
            class_schema=class_schema,
            instance_schema=instance_schema,
            simplifier=simplifier,
            converter={
                Smart: from_smart,
                str: from_str,
            },
        )

    def test__class(self) -> None:
        cls = ParentC
        expected = {
            'class': 'tests.commons.classes.ParentC',
            'positional': 'str???',
            'keyword': 'float???',
        }

        actual = instance_schema(Smart.register, cls, tuple(), False)

        self.assertEqual(expected, actual)

    def test__dataclass(self) -> None:
        cls = make_dataclass(
            'DataClass',
            fields=(
                ('a', int, field()),
                ('b', int, field(init=False)),
                ('c', int, field(default=5)),
                ('d', dict[str, int], field(default_factory=lambda: {'x': 5})),
            ),
        )
        expected = {
            'class': 'types.DataClass',
            'a': 'int???',
            'c': 5,
            'd': {'x': 5},
        }

        actual = instance_schema(Smart.register, cls, tuple(), False)

        self.assertEqual(expected, actual)

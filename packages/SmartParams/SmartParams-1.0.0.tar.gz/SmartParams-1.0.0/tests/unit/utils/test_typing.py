import inspect
import types
from typing import Any, Union

from smartparams import Smart
from smartparams.utils.typing import class_hierarchy, get_return_type, get_type_hints
from tests.commons.classes import ChildA, ParentA, ParentB, any_type_function
from tests.unit import UnitTest


class TestGetTypeHints(UnitTest):
    def test(self) -> None:
        signature = inspect.signature(any_type_function)
        expected = {'a': str, 'b': Any, 'c': tuple[bool, ...], 'd': int, 'e': dict[str, float]}

        actual = get_type_hints(signature.parameters)

        self.assertEqual(expected, actual)


class TestGetReturnType(UnitTest):
    def test__class(self) -> None:
        expected = ParentA

        actual = get_return_type(ParentA)

        self.assertEqual(expected, actual)

    def test__function(self) -> None:
        expected = bytes

        actual = get_return_type(any_type_function)

        self.assertEqual(expected, actual)


class TestClassHierarchy(UnitTest):
    def test(self) -> None:
        expected = ((ParentA, ()), (ChildA, ()), (Smart, (ParentB,)))

        actual = class_hierarchy(Union[ParentA, Smart[ParentB]])

        self.assertIsInstance(actual, types.GeneratorType)
        self.assertEqual(expected, tuple(actual))

    def test__none(self) -> None:
        expected = ((type(None), ()),)

        actual = class_hierarchy(None)

        self.assertIsInstance(actual, types.GeneratorType)
        self.assertEqual(expected, tuple(actual))

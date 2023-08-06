import inspect
from abc import ABCMeta, abstractmethod
from typing import Any

from typeguard import check_type

from smartparams import Smart
from smartparams.register import SmartRegister
from smartparams.utils.typing import class_hierarchy, get_return_type, get_type_hints
from tests.unit import UnitTest


class Types:
    class Test(UnitTest, metaclass=ABCMeta):
        CLS: Any
        DEFAULT: Any
        MAP_VALUES: dict[str, Any]
        CONVERT_VALUES: dict[Any, Any]
        SUBTYPES: tuple[Any, ...] = ()

        def setUp(self) -> None:
            self.register = SmartRegister()
            self.init_register()

        @abstractmethod
        def init_register(self) -> None:
            pass

        def test__test_name(self) -> None:
            expected = self.__class__.__name__

            actual = 'Test' + self.CLS.__name__[0].upper() + self.CLS.__name__[1:]

            self.assertEqual(expected, actual)

        def test__global_existence(self) -> None:
            self.assertTrue(self.register.has_class(self.CLS))
            self.assertTrue(Smart.register.has_class(self.CLS))

        def assert_expected_type(
            self,
            value: Any,
            expected_type: Any,
        ) -> None:
            try:
                check_type(
                    argname=str(value),
                    value=value,
                    expected_type=expected_type,
                )
            except TypeError:
                self.assertTrue(False, msg=f"value {value} has not type {expected_type}")
            else:
                self.assertTrue(True)

        def test__class_schema(self) -> None:
            if not self.register.has_class_schema(self.CLS):
                self.skipTest("there is not class schema")

            schema = self.register.get_class_schema(self.CLS)

            signature = inspect.signature(schema)
            type_hints = get_type_hints(signature.parameters)
            expected = get_return_type(schema)
            actual = schema(self.register, self.SUBTYPES, False)

            self.assertIsInstance(actual, (type(None), bool, int, float, str, list, dict))
            self.assert_expected_type(actual, expected)
            self.assertEqual(('self', 'subtypes', 'skip_default'), tuple(type_hints))

        def test__class_schema__reversed(self) -> None:
            if not Smart.register.has_class_schema(self.CLS):
                self.skipTest("there is not class schema")

            self.assertTrue(self.register.has_class_schema(self.CLS))
            self.assertIs(
                self.register.get_class_schema(self.CLS),
                Smart.register.get_class_schema(self.CLS),
            )

        def test__instance_schema(self) -> None:
            if not self.register.has_instance_schema(self.CLS):
                self.skipTest("there is not instance schema")

            schema = self.register.get_instance_schema(self.CLS)

            signature = inspect.signature(schema)
            type_hints = get_type_hints(signature.parameters)
            expected = get_return_type(schema)
            actual = schema(self.register, self.DEFAULT, self.SUBTYPES, False)

            self.assertIsInstance(actual, (type(None), bool, int, float, str, list, dict))
            self.assert_expected_type(actual, expected)
            self.assertEqual(('self', 'instance', 'subtypes', 'skip_default'), tuple(type_hints))

        def test__instance_schema__reversed(self) -> None:
            if not Smart.register.has_instance_schema(self.CLS):
                self.skipTest("there is not instance schema")

            self.assertTrue(self.register.has_instance_schema(self.CLS))
            self.assertIs(
                self.register.get_instance_schema(self.CLS),
                Smart.register.get_instance_schema(self.CLS),
            )

        def test__simplifier(self) -> None:
            if not self.register.has_simplifier(self.CLS):
                self.skipTest("there is not simplifier")

            simplifier = self.register.get_simplifier(self.CLS)

            signature = inspect.signature(simplifier)
            type_hints = get_type_hints(signature.parameters)
            expected = get_return_type(simplifier)
            actual = simplifier(self.register, self.DEFAULT, False, False)

            self.assertIsInstance(actual, (type(None), bool, int, float, str, list, dict))
            self.assert_expected_type(actual, expected)
            self.assertEqual(('self', 'default', 'skip_default', 'strict'), tuple(type_hints))
            self.assert_expected_type(self.DEFAULT, self.CLS)
            self.assert_expected_type(self.DEFAULT, type_hints['default'])

        def test__simplifier__reversed(self) -> None:
            if not Smart.register.has_simplifier(self.CLS):
                self.skipTest("there is not simplifier")

            self.assertTrue(self.register.has_simplifier(self.CLS))
            self.assertIs(
                self.register.get_simplifier(self.CLS),
                Smart.register.get_simplifier(self.CLS),
            )

        def test__mapper(self) -> None:
            for name, mapper in self.register.objects[self.CLS].mapper.items():
                with self.subTest(name=name):
                    signature = inspect.signature(self.CLS)
                    type_hints = get_type_hints(signature.parameters)
                    expected = get_return_type(mapper)
                    actual = mapper(self.MAP_VALUES[name])

                    self.assertIs(self.CLS, self.CLS)
                    self.assertIn(name, type_hints)
                    self.assert_expected_type(actual, type_hints[name])
                    self.assertIn(
                        expected,
                        [cls for cls, _ in class_hierarchy(type_hints[name])],
                    )
                    self.assertTrue(Smart.register.has_mapper(self.CLS, name))
                    self.assertIs(mapper, Smart.register.get_mapper(self.CLS, name))

        def test__mapper__reversed(self) -> None:
            if not self.register.has_class(self.CLS):
                self.skipTest("there is not registered class")

            for name, mapper in Smart.register.objects[self.CLS].mapper.items():
                with self.subTest(name=name):
                    self.assertTrue(self.register.has_mapper(self.CLS, name))
                    self.assertIs(mapper, self.register.get_mapper(self.CLS, name))

        def test__converter(self) -> None:
            for from_type, converter in self.register.objects[self.CLS].converter.items():
                with self.subTest(from_type=from_type):
                    signature = inspect.signature(converter)
                    type_hints = get_type_hints(signature.parameters)
                    expected = get_return_type(converter)
                    actual = converter(self.register, self.CONVERT_VALUES[from_type], self.SUBTYPES)

                    self.assert_expected_type(actual, expected)
                    self.assert_expected_type(actual, self.CLS)
                    self.assertEqual(('self', 'argument', 'subtypes'), tuple(type_hints))
                    self.assertIs(from_type, type_hints['argument'])
                    self.assertTrue(Smart.register.has_converter(self.CLS, from_type))
                    self.assertIs(converter, Smart.register.get_converter(self.CLS, from_type))

        def test__converter__reversed(self) -> None:
            if not self.register.has_class(self.CLS):
                self.skipTest("there is not registered class")

            for from_type, converter in Smart.register.objects[self.CLS].converter.items():
                with self.subTest(from_type=from_type):
                    self.assertTrue(self.register.has_converter(self.CLS, from_type))
                    self.assertIs(converter, self.register.get_converter(self.CLS, from_type))

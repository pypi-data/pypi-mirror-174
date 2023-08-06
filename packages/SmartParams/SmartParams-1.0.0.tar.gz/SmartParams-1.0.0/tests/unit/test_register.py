from pathlib import Path
from unittest.mock import Mock, patch

from smartparams.register import SmartRegister
from tests.commons.classes import ChildA, ParentA, equation, to_upper_case
from tests.unit import UnitTest


class TestSmartRegister(UnitTest):
    def setUp(self) -> None:
        self.register = SmartRegister()

        self.cls = Mock(__qualname__='MockName')
        self.name = 'MockName'
        self.path = 'unittest.mock.MockName'
        self.class_schema = Mock()
        self.instance_schema = Mock()
        self.simplifier = Mock()
        self.smartifier = Mock()
        self.mapper = {'arg1': Mock(), 'arg2': Mock()}
        self.converter = {str: Mock(), int: Mock()}

        self.register(
            cls=self.cls,
            class_schema=self.class_schema,  # type: ignore
            instance_schema=self.instance_schema,  # type: ignore
            simplifier=self.simplifier,  # type: ignore
            smartifier=self.smartifier,  # type: ignore
            mapper=self.mapper,  # type: ignore
            converter=self.converter,  # type: ignore
        )

    def test__call_register(self) -> None:
        self.assertEqual(1, len(self.register.objects))
        obj = self.register.objects[self.cls]
        self.assertEqual(self.cls, obj.cls)
        self.assertEqual(self.name, obj.name)
        self.assertEqual(self.class_schema, obj.class_schema)
        self.assertEqual(self.instance_schema, obj.instance_schema)
        self.assertEqual(self.simplifier, obj.simplifier)
        self.assertEqual(self.smartifier, obj.smartifier)
        self.assertEqual(self.mapper, obj.mapper)
        self.assertEqual(self.converter, obj.converter)

    def test__call_register__override(self) -> None:
        class_schema = Mock()
        instance_schema = Mock()
        simplifier = Mock()
        smartifier = Mock()
        mapper = {'arg1': Mock()}
        converter = {str: Mock()}
        obj = self.register.objects[self.cls]
        expected_mapper = dict(obj.mapper)
        expected_mapper.update(mapper)
        expected_converter = dict(obj.converter)
        expected_converter.update(converter)

        self.register(
            cls=self.cls,
            class_schema=class_schema,  # type: ignore
            instance_schema=instance_schema,  # type: ignore
            simplifier=simplifier,  # type: ignore
            smartifier=smartifier,  # type: ignore
            mapper=mapper,  # type: ignore
            converter=converter,  # type: ignore
        )

        self.assertEqual(self.cls, obj.cls)
        self.assertEqual(self.name, obj.name)
        self.assertEqual(class_schema, obj.class_schema)
        self.assertEqual(instance_schema, obj.instance_schema)
        self.assertEqual(simplifier, obj.simplifier)
        self.assertEqual(smartifier, obj.smartifier)
        self.assertEqual(expected_mapper, obj.mapper)
        self.assertEqual(expected_converter, obj.converter)

    def test__call_register__add_mapper_and_converter(self) -> None:
        mapper = {'arg3': Mock()}
        converter = {float: Mock()}
        obj = self.register.objects[self.cls]
        expected_mapper = dict(obj.mapper)
        expected_mapper.update(mapper)
        expected_converter = dict(obj.converter)
        expected_converter.update(converter)

        self.register(
            cls=self.cls,
            mapper=mapper,  # type: ignore
            converter=converter,  # type: ignore
        )

        self.assertEqual(expected_mapper, obj.mapper)
        self.assertEqual(expected_converter, obj.converter)

    def test__call_register__change_name(self) -> None:
        cls = self.cls
        name = 'NewName'

        self.register(
            cls=cls,
            name=name,
        )

        obj = self.register.objects[self.cls]
        self.assertEqual(cls, obj.cls)
        self.assertEqual(name, obj.name)

    def test__call_register__change_name__raise_value_error(self) -> None:
        name = 'NewName'
        cls = Mock(__qualname__=name)
        self.register(cls)

        self.assertRaises(ValueError, self.register, self.cls, name=name)

    def test__call_register__duplicate_name__raise_value_error(self) -> None:
        cls = Mock(__qualname__='MockName')

        self.assertRaises(ValueError, self.register, cls)

    def test__call_register__wrapper(self) -> None:
        cls = Mock(__qualname__='NewMockName')
        name = 'Mock'

        register = self.register(name=name)
        register(cls)

        obj = self.register.objects[cls]
        self.assertEqual(cls, obj.cls)
        self.assertEqual(name, obj.name)

    def test__call_register_many(self) -> None:
        actual = self.register((equation, ParentA))

        self.assertTrue((equation, ParentA, ChildA), tuple(actual))
        self.assertTrue(self.register.has_class(equation))
        self.assertTrue(self.register.has_class(ParentA))
        self.assertTrue(self.register.has_class(ChildA))

    def test__call_register_many__duplicated_class(self) -> None:
        actual = self.register((self.cls,))

        self.assertFalse(actual)

    def test__call_register_many__duplicated_name(self) -> None:
        actual = self.register((Mock(__qualname__=self.name),))

        self.assertFalse(actual)

    def test__call_register_many__keyword_argument(self) -> None:
        self.assertRaises(ValueError, self.register, tuple(), name='name')

    def test_str(self) -> None:
        self.assertEqual(f'SmartRegister[{self.name}]', str(self.register))

    def test_clear(self) -> None:
        self.register.objects[Mock()] = Mock()  # type: ignore
        self.register.resolvers.append(Mock())  # type: ignore

        self.register.clear()

        self.assertFalse(self.register.objects)
        self.assertFalse(self.register.resolvers)

    def test_objects(self) -> None:
        objects = self.register.objects

        self.assertEqual(self.register.objects, objects)
        self.assertIs(self.register.objects, objects)

    def test_has_class(self) -> None:
        actual = self.register.has_class(self.cls)

        self.assertTrue(actual)

    def test_has_name(self) -> None:
        actual = self.register.has_name(self.name)

        self.assertTrue(actual)

    def test_has_schema(self) -> None:
        actual = self.register.has_class_schema(self.cls)

        self.assertTrue(actual)

    def test_has_simplifier(self) -> None:
        actual = self.register.has_simplifier(self.cls)

        self.assertTrue(actual)

    def test_has_smartifier(self) -> None:
        actual = self.register.has_smartifier(self.cls)

        self.assertTrue(actual)

    def test_has_mapper(self) -> None:
        actual = self.register.has_mapper(self.cls, 'arg1')

        self.assertTrue(actual)

    def test_has_converter(self) -> None:
        actual = self.register.has_converter(self.cls, str)

        self.assertTrue(actual)

    def test_get_class_by_name(self) -> None:
        expected = self.cls

        actual = self.register.get_class_by_name(self.name)

        self.assertEqual(expected, actual)

    def test_get_class_by_name__raise_key_error(self) -> None:
        self.assertRaises(KeyError, self.register.get_class_by_name, Mock)

    def test_get_class_by_path(self) -> None:
        expected = self.cls

        actual = self.register.get_class_by_path(self.path)

        self.assertEqual(expected, actual)

    def test_get_class_by_path__raise_key_error(self) -> None:
        self.assertRaises(KeyError, self.register.get_class_by_path, Mock)

    def test_get_name(self) -> None:
        expected = self.name

        actual = self.register.get_name(self.cls)

        self.assertEqual(expected, actual)

    def test_get_class_schema(self) -> None:
        expected = self.class_schema

        actual = self.register.get_class_schema(self.cls)

        self.assertEqual(expected, actual)

    def test_get_class_schema__raise_value_error(self) -> None:
        self.register.objects[self.cls].class_schema = None

        self.assertRaises(ValueError, self.register.get_class_schema, self.cls)

    def test_get_instance_schema(self) -> None:
        expected = self.instance_schema

        actual = self.register.get_instance_schema(self.cls)

        self.assertEqual(expected, actual)

    def test_get_instance_schema__raise_value_error(self) -> None:
        self.register.objects[self.cls].instance_schema = None

        self.assertRaises(ValueError, self.register.get_instance_schema, self.cls)

    def test_get_simplifier(self) -> None:
        expected = self.simplifier

        actual = self.register.get_simplifier(self.cls)

        self.assertEqual(expected, actual)

    def test_get_simplifier_raise_value_error(self) -> None:
        self.register.objects[self.cls].simplifier = None

        self.assertRaises(ValueError, self.register.get_simplifier, self.cls)

    def test_get_smartifier(self) -> None:
        expected = self.smartifier

        actual = self.register.get_smartifier(self.cls)

        self.assertEqual(expected, actual)

    def test_get_smartifier_raise_value_error(self) -> None:
        self.register.objects[self.cls].smartifier = None

        self.assertRaises(ValueError, self.register.get_smartifier, self.cls)

    def test_get_mapper(self) -> None:
        expected = self.mapper['arg1']

        actual = self.register.get_mapper(self.cls, 'arg1')

        self.assertEqual(expected, actual)

    def test_get_mapper_raise_key_error(self) -> None:
        self.register.objects[self.cls].mapper.pop('arg1')

        self.assertRaises(KeyError, self.register.get_mapper, self.cls, 'arg1')

    def test_get_converter(self) -> None:
        expected = self.converter[str]

        actual = self.register.get_converter(self.cls, str)

        self.assertEqual(expected, actual)

    def test_get_converter_raise_key_error(self) -> None:
        self.register.objects[self.cls].converter.pop(str)

        self.assertRaises(KeyError, self.register.get_converter, self.cls, str)

    def test_class_name(self) -> None:
        data = Mock
        expected = 'Mock'

        actual = self.register.class_name(data)

        self.assertEqual(expected, actual)

    def test_class_name__raise_value_error(self) -> None:
        data = Mock()

        self.assertRaises(ValueError, self.register.class_name, data)

    def test_class_path(self) -> None:
        data = equation
        expected = 'tests.commons.classes.equation'

        actual = self.register.class_path(data)

        self.assertEqual(expected, actual)

    def test_class_path__raises_value_error(self) -> None:
        self.assertRaises(ValueError, self.register.class_path, 'unknown')

    def test_import_class__by_name(self) -> None:
        data = self.name

        actual = self.register.import_class(data)

        self.assertEqual(self.cls, actual)

    def test_import_class__by_path(self) -> None:
        data = self.path

        actual = self.register.import_class(data)

        self.assertEqual(self.cls, actual)

    @patch('smartparams.register.import_class')
    def test_import_class(self, import_class: Mock) -> None:
        data = 'some.class'
        import_class.return_value = 'class'

        actual = self.register.import_class(data)

        import_class.assert_called_with(data)
        self.assertEqual('class', actual)

    def test_import_class__registered(self) -> None:
        actual = self.register.import_class(self.name)

        self.assertIs(actual, self.cls)

    @patch('smartparams.register.autodiscover')
    def test_autodiscover(self, autodiscover: Mock) -> None:
        path = 'path/file.txt'
        include = Mock()
        exclude = Mock()
        autodiscover.return_value = []

        actual = self.register.autodiscover(
            path=path,
            include=include,
            exclude=exclude,
        )

        self.assertEqual([], actual)
        autodiscover.assert_called_with(path=Path(path), include=include, exclude=exclude)

    def test_instantiate(self) -> None:
        cls = Mock(__module__='module', __qualname__='Mock')
        args = ('a',)
        kwargs = {'b': 1}
        expected = cls('a', b=1)

        actual = self.register.instantiate(cls, args, kwargs)

        self.assertEqual(expected, actual)

    def test_instantiate__unknown_signature(self) -> None:
        cls = dict
        kwargs = {'b': 1}
        expected = {'b': 1}

        actual = self.register.instantiate(cls, tuple(), kwargs)

        self.assertEqual(expected, actual)

    def test_instantiate__wrong_signature(self) -> None:
        cls = to_upper_case
        args = ('a',)
        kwargs = {'b': 1}

        self.assertRaises(TypeError, self.register.instantiate, cls, args, kwargs)

    def test_instantiate__mapping(self) -> None:
        cls = to_upper_case
        self.register(to_upper_case, mapper={'x': str})
        kwargs = {'x': 1}
        expected = '1'

        actual = self.register.instantiate(cls, tuple(), kwargs)

        self.assertEqual(expected, actual)

    def test_instantiate__mapping__raise_exception(self) -> None:
        cls = to_upper_case
        self.register(to_upper_case, mapper={'x': lambda argument: 1 / 0})
        kwargs = {'x': 1}

        self.assertRaises(ZeroDivisionError, self.register.instantiate, cls, tuple(), kwargs)

    def test_instantiate__convert(self) -> None:
        cls = to_upper_case
        self.register(str, converter={int: lambda register, argument, subtypes: str(argument)})
        kwargs = {'x': 1}
        expected = '1'

        actual = self.register.instantiate(cls, tuple(), kwargs)

        self.assertEqual(expected, actual)

    def test_instantiate__convert__raise_exception(self) -> None:
        cls = to_upper_case
        self.register(str, converter={int: lambda register, argument, subtypes: 1 / 0})
        kwargs = {'x': 1}

        self.assertRaises(ZeroDivisionError, self.register.instantiate, cls, tuple(), kwargs)

    def test_instantiate__positional_arguments(self) -> None:
        cls = equation
        args = ('a',)
        kwargs = {'b': 1}
        expected = 'a=1'

        actual = self.register.instantiate(cls, args, kwargs)

        self.assertEqual(expected, actual)

    @patch('smartparams.register.Log')
    def test_instantiate__type_check(self, log: Mock) -> None:
        cls = equation
        args = ('a',)
        kwargs = {'b': '1'}
        expected = 'a=1'

        actual = self.register.instantiate(cls, args, kwargs)

        self.assertEqual(expected, actual)
        log.init.error.assert_called_once()

    def test_convert__same_type(self) -> None:
        argument = 'argument'
        expected_type = str
        converter = Mock()
        self.register(str, converter={str: converter})

        actual = self.register.convert(argument, expected_type)

        converter.assert_called_with(self.register, argument, tuple())
        self.assertEqual(converter(), actual)

    @patch('smartparams.register.Log')
    def test_convert__multiple_converters(self, log: Mock) -> None:
        argument = 'argument'
        expected_type = int | float
        converter = Mock()
        self.register(int, converter={str: converter})
        self.register(float, converter={str: converter})

        self.register.convert(argument, expected_type)

        self.assertEqual(2, log.init.debug.call_count)

    def test_simplify__registered_class(self) -> None:
        cls = str
        self.register(str)
        expected = 'str'

        actual = self.register.simplify(cls)

        self.assertEqual(expected, actual)

    def test_schema__missing_value(self) -> None:
        value = Mock()
        expected = '???'

        actual = self.register.schema(value=value)

        self.assertEqual(expected, actual)

    def test_schema__registered_class(self) -> None:
        value = str
        self.register(str)
        expected = 'str'

        actual = self.register.schema(value=value)

        self.assertEqual(expected, actual)

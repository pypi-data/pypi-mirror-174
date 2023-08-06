import types
from typing import ItemsView, KeysView, ValuesView
from unittest.mock import Mock, patch

from smartparams import Smart
from tests.commons.classes import ChildA, ParentA, some_function, square
from tests.unit import UnitTest


class TestSmartInit(UnitTest):
    def test__none(self) -> None:
        smart: Smart = Smart()

        self.assertFalse(smart)
        self.assertNotIn('class', smart)

    def test__str(self) -> None:
        data = 'Class'

        smart: Smart = Smart(data)

        self.assertTrue(smart)
        self.assertEqual('Class', smart['class'])

    def test__callable(self) -> None:
        smart: Smart = Smart(some_function)

        self.assertTrue(smart)
        self.assertEqual(some_function, smart['class'])

    def test__mapping(self) -> None:
        data = {'a': 15, 'c': dict(f=True)}

        smart: Smart = Smart(data)

        self.assertEqual(15, smart['a'])
        self.assertEqual(dict(f=True), smart['c'])
        self.assertIsInstance(smart['c'], Smart)

    def test__iterable(self) -> None:
        data = ['a=15', ('c', dict(f=True))]

        smart: Smart = Smart(data)  # type: ignore

        self.assertEqual(15, smart['a'])
        self.assertEqual(dict(f=True), smart['c'])
        self.assertIsInstance(smart['c'], Smart)

    def test__kwargs(self) -> None:
        data = {'a': 15, 'c': dict(f=True)}

        smart: Smart = Smart(data)

        self.assertEqual(15, smart['a'])
        self.assertEqual(dict(f=True), smart['c'])
        self.assertIsInstance(smart['c'], Smart)

    def test__incorrect_type(self) -> None:
        self.assertRaises(TypeError, Smart, 15)


class TestSmartDict(UnitTest):
    def setUp(self) -> None:
        self.smart: Smart = Smart(a=10, b='x', c={'e': True, 'f': False}, d=[1, 2, 3])

    def test_getitem(self) -> None:
        expected = True

        actual = self.smart['c.e']

        self.assertEqual(expected, actual)

    def test_getitem__no_key(self) -> None:
        self.assertRaises(KeyError, self.smart.__getitem__, 'c.x')

    def test_getitem__key_not_dict(self) -> None:
        self.assertRaises(KeyError, self.smart.__getitem__, 'a.x')

    def test_getitem__register(self) -> None:
        expected = self.smart.copy()
        expected['class'] = ChildA

        actual = self.smart[ChildA]

        self.assertEqual(expected, actual)
        self.assertFalse(self.smart.register.has_class(ChildA))
        self.assertTrue(actual.register.has_class(ChildA))

    def test_getattr(self) -> None:
        expected = True

        actual = self.smart.c.e

        self.assertEqual(expected, actual)

    def test_getattr__no_key__key_error(self) -> None:
        with self.assertRaises(KeyError):
            self.smart.c.x  # noqa

    def test_setitem(self) -> None:
        data = 'false'
        expected = 'false'

        self.smart['c.e'] = data

        self.assertEqual(expected, self.smart['c.e'])

    def test_setitem__no_key(self) -> None:
        data = 'false'
        expected = 'false'

        self.smart['c.x'] = data

        self.assertIn('c.x', self.smart)
        self.assertEqual(expected, self.smart['c.x'])

    def test_setitem__no_string_value(self) -> None:
        self.assertRaises(TypeError, self.smart.__setitem__, 1, 'one')

    def test_setattr(self) -> None:
        data = 'false'
        expected = 'false'

        self.smart.c.e = data

        self.assertEqual(expected, self.smart['c.e'])

    def test_setattr__no_key(self) -> None:
        data = 'false'
        expected = 'false'

        self.smart.c.x = data

        self.assertIn('c.x', self.smart)
        self.assertEqual(expected, self.smart['c.x'])

    def test_delitem(self) -> None:
        del self.smart['c.e']

        self.assertNotIn('c.e', self.smart)
        self.assertIn('c.f', self.smart)

    def test_delitem__no_key(self) -> None:
        self.assertRaises(KeyError, self.smart.__delitem__, 'c.x')

    def test_delitem__key_not_dict(self) -> None:
        self.assertRaises(KeyError, self.smart.__delitem__, 'a.x')

    def test_iter(self) -> None:
        expected = ['a', 'b', 'c', 'd']

        actual = [key for key in self.smart]

        self.assertEqual(expected, actual)

    def test_contains__expect_true(self) -> None:
        actual = 'c.e' in self.smart

        self.assertTrue(actual)

    def test_contains__expect_false(self) -> None:
        actual = 'c.x' in self.smart

        self.assertFalse(actual)

    def test_keys(self) -> None:
        expected = ('a', 'b', 'c', 'd')

        actual = self.smart.keys()

        self.assertIsInstance(actual, KeysView)
        self.assertIsInstance(actual, type({}.keys()))
        self.assertEqual(expected, tuple(actual))

    def test_values(self) -> None:
        expected = (10, 'x', {'e': True, 'f': False}, [1, 2, 3])

        actual = self.smart.values()

        self.assertIsInstance(actual, ValuesView)
        self.assertIsInstance(actual, type({}.values()))
        self.assertEqual(expected, tuple(actual))

    def test_items(self) -> None:
        expected = (('a', 10), ('b', 'x'), ('c', {'e': True, 'f': False}), ('d', [1, 2, 3]))

        actual = self.smart.items()

        self.assertIsInstance(actual, ItemsView)
        self.assertIsInstance(actual, type({}.items()))
        self.assertEqual(expected, tuple(actual))

    def test_keys__flatten(self) -> None:
        expected = ('a', 'b', 'c.e', 'c.f', 'd')

        actual = self.smart.keys(flatten=True)

        self.assertIsInstance(actual, KeysView)
        self.assertIsInstance(actual, type({}.keys()))
        self.assertEqual(expected, tuple(actual))

    def test_values__flatten(self) -> None:
        expected = (10, 'x', True, False, [1, 2, 3])

        actual = self.smart.values(flatten=True)

        self.assertIsInstance(actual, ValuesView)
        self.assertIsInstance(actual, type({}.values()))
        self.assertEqual(expected, tuple(actual))

    def test_items__flatten(self) -> None:
        expected = (('a', 10), ('b', 'x'), ('c.e', True), ('c.f', False), ('d', [1, 2, 3]))

        actual = self.smart.items(flatten=True)

        self.assertIsInstance(actual, ItemsView)
        self.assertIsInstance(actual, type({}.items()))
        self.assertEqual(expected, tuple(actual))

    def test_get(self) -> None:
        expected = True

        actual = self.smart.get('c.e')

        self.assertEqual(expected, actual)

    def test_get__default_none(self) -> None:
        actual = self.smart.get('c.x')

        self.assertIsNone(actual)

    def test_get__default_custom(self) -> None:
        expected = 'default'

        actual = self.smart.get('c.x', 'default')

        self.assertEqual(expected, actual)

    def test_get__no_dict_default(self) -> None:
        expected = 'default'

        actual = self.smart.get('a.x', 'default')

        self.assertEqual(expected, actual)

    def test_pop(self) -> None:
        expected = True

        actual = self.smart.pop('c.e')

        self.assertEqual(expected, actual)
        self.assertNotIn('c.e', self.smart)
        self.assertIn('c.f', self.smart)

    def test_pop__no_item(self) -> None:
        self.assertRaises(KeyError, self.smart.pop, 'c.x')

    def test_pop__default(self) -> None:
        expected = 'default'

        actual = self.smart.pop('c.x', 'default')

        self.assertEqual(expected, actual)
        self.assertNotIn('c.x', self.smart)
        self.assertIn('c.f', self.smart)

    def test_pop__no_dict(self) -> None:
        self.assertRaises(KeyError, self.smart.pop, 'a.x')

    def test_pop__no_dict_default(self) -> None:
        expected = 'default'

        actual = self.smart.pop('a.x', 'default')

        self.assertEqual(expected, actual)
        self.assertNotIn('a.x', self.smart)
        self.assertIn('a', self.smart)

    def test_update__mapping(self) -> None:
        data = {'a': 15, 'c': dict(f=True)}

        self.smart.update(data)

        self.assertEqual(15, self.smart['a'])
        self.assertEqual('x', self.smart['b'])
        self.assertEqual(dict(f=True), self.smart['c'])
        self.assertIsInstance(self.smart['c'], Smart)

    def test_update__iterable(self) -> None:
        data = ['a=15', ('c', dict(f=True))]

        self.smart.update(data)  # type: ignore

        self.assertEqual(15, self.smart['a'])
        self.assertEqual('x', self.smart['b'])
        self.assertEqual(dict(f=True), self.smart['c'])
        self.assertIsInstance(self.smart['c'], Smart)

    def test_update__kwargs(self) -> None:
        data = {'a': 15, 'c': dict(f=True)}

        self.smart.update(**data)

        self.assertEqual(15, self.smart['a'])
        self.assertEqual('x', self.smart['b'])
        self.assertEqual(dict(f=True), self.smart['c'])
        self.assertIsInstance(self.smart['c'], Smart)

    def test_update__incorrect_type(self) -> None:
        self.assertRaises(TypeError, self.smart.update, 'incorrect_type')

    def test_merge(self) -> None:
        smart: Smart = Smart({'a': 15, 'c': {'e': 5, 'g': 10}, 'd': [4, 5, 6], 'y': 'z'})
        expected: Smart = Smart(
            {
                'a': 15,
                'b': 'x',
                'c': {'e': 5, 'f': False, 'g': 10},
                'd': [1, 2, 3, 4, 5, 6],
                'y': 'z',
            }
        )
        expected_smart = smart.copy()
        expected_self_smart = self.smart.copy()

        actual = Smart.merge(self.smart, smart)

        self.assertEqual(expected, actual)
        self.assertEqual(expected_smart, smart)
        self.assertEqual(expected_self_smart, self.smart)
        self.assertIsNot(smart, actual)
        self.assertIsNot(self.smart, actual)

    def test_copy(self) -> None:
        actual = self.smart.copy()

        self.assertEqual(self.smart, actual)
        self.assertIsNot(self.smart, actual)
        self.assertIsNot(self.smart['d'], actual['d'])

    def test_explode(self) -> None:
        actual = self.smart.explode('d')

        self.assertIsInstance(actual, types.GeneratorType)
        result = tuple(actual)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0]['d'])

    def test_explode__type_error(self) -> None:
        with self.assertRaises(TypeError):
            tuple(self.smart.explode('d', 'a'))


class TestSmartPartial(UnitTest):
    def setUp(self) -> None:
        self.smart: Smart[ParentA] = Smart(ParentA, arg1='a')

    def test_call(self) -> None:
        actual = self.smart(arg2=99)

        self.assertIsInstance(actual, ParentA)
        self.assertEqual('a', actual.arg1)
        self.assertEqual(99, actual.arg2)

    @patch('smartparams.smart.Log')
    def test_call__override_parameters(self, log: Mock) -> None:
        actual = self.smart(arg1='b')

        self.assertIsInstance(actual, ParentA)
        self.assertEqual('b', actual.arg1)
        self.assertEqual(5, actual.arg2)
        log.init.warning.assert_called_once()

    def test_params(self) -> None:
        self.smart[''] = 'empty_key'
        expected = {'arg1': 'a', '': 'empty_key'}

        actual = self.smart.params

        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, Smart)

    def test_type__class(self) -> None:
        actual = self.smart.type

        self.assertIs(actual, ParentA)

    def test_type__function(self) -> None:
        smart: Smart[int] = Smart(square)

        actual = smart.type

        self.assertIs(actual, int)

    def test_cls__class(self) -> None:
        actual = self.smart.cls

        self.assertIs(actual, ParentA)

    def test_cls__function(self) -> None:
        smart: Smart[int] = Smart(square)

        actual = smart.cls

        self.assertIs(actual, square)

    def test_cls__string(self) -> None:
        smart: Smart[int] = Smart('tests.commons.classes.square')

        actual = smart.cls

        self.assertIs(actual, square)

    def test_cls__none__key_error(self) -> None:
        smart: Smart = Smart()

        with self.assertRaises(KeyError):
            smart.cls  # noqa

    def test_cls__type_error(self) -> None:
        self.smart['class'] = 12

        with self.assertRaises(TypeError):
            self.smart.cls  # noqa

    def test_cls__setter(self) -> None:
        self.smart.cls = ChildA

        self.assertIs(self.smart.cls, ChildA)

    def test_cls__setter__type_error(self) -> None:
        with self.assertRaises(TypeError):
            self.smart.cls = 5  # type: ignore

    def test_cls__deleter(self) -> None:
        del self.smart.cls

        self.assertNotIn('class', self.smart)

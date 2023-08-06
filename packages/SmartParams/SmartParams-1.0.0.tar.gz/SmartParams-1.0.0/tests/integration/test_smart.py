import pickle as pkl
from pathlib import Path
from unittest.mock import Mock, patch

from smartparams import Smart
from tests.commons.classes import ParentB, some_function
from tests.integration import IntegrationTest


class TestSerialization(IntegrationTest):
    def setUp(self) -> None:
        self.smart: Smart[ParentB] = Smart(
            ParentB,
            **{
                'smart': {'a': 12, 3: True},
                'smart_a': Smart({'class': 'ChildA', 'arg1': 'argument1'}),
                'object_a': Smart({'class': 'ChildA', 'arg1': 'argument1', 'arg2': 10}),
                'type_a': 'ChildA',
                'any_type': some_function,
            },
        )

    def test__pickle(self) -> None:
        pickled = pkl.dumps(self.smart)
        smart = pkl.loads(pickled)

        self.assertIsInstance(smart, Smart)
        self.assertEqual(self.smart, smart)
        self.assertEqual(str(self.smart), str(smart))
        self.assertIs(smart.type, ParentB)
        self.assertEqual(self.smart.register.class_keyword, smart.register.class_keyword)
        self.assertEqual(self.smart.register.missing_value, smart.register.missing_value)
        self.assertEqual(self.smart.register.objects, smart.register.objects)


class TestSmartIO(IntegrationTest):
    def setUp(self) -> None:
        self.smart: Smart[ParentB] = Smart(ParentB)

    @patch('smartparams.smart.yaml.load')
    def test_load__yaml(self, load: Mock) -> None:
        path = Path('path/to/file.yaml')
        expected = {'a': 10}
        load.return_value = expected

        actual = Smart.load(path)

        self.assertIsInstance(actual, Smart)
        self.assertEqual(expected, actual)

    @patch('smartparams.smart.yaml.load')
    def test_load__yml(self, load: Mock) -> None:
        path = Path('path/to/file.yml')
        expected = {'a': 10}
        load.return_value = expected

        actual = Smart.load(path)

        self.assertIsInstance(actual, Smart)
        self.assertEqual(expected, actual)

    @patch('smartparams.smart.json.load')
    def test_load__json(self, load: Mock) -> None:
        path = Path('path/to/file.json')
        expected = {'a': 10}
        load.return_value = expected

        actual = Smart.load(path)

        self.assertIsInstance(actual, Smart)
        self.assertEqual(expected, actual)

    def test_load__unknown_format__value_error(self) -> None:
        self.assertRaises(ValueError, Smart.load, Path('path/to/file.txt'))

    @patch('smartparams.smart.yaml.load')
    def test_load__not_dict__value_error(self, load: Mock) -> None:
        path = Path('path/to/file.yaml')
        load.return_value = [1, 2, 3]

        self.assertRaises(ValueError, Smart.load, path)

    @patch('smartparams.smart.yaml.save')
    def test_save__yaml(self, save: Mock) -> None:
        expected_data = {'class': 'tests.commons.classes.ParentB'}
        path = Path('path/to/file.yaml')

        self.smart.save(path)

        save.assert_called_with(
            data=expected_data,
            path=path,
        )

    @patch('smartparams.smart.yaml.save')
    def test_save__yml(self, save: Mock) -> None:
        expected_data = {'class': 'tests.commons.classes.ParentB'}
        path = Path('path/to/file.yml')

        self.smart.save(path)

        save.assert_called_with(
            data=expected_data,
            path=path,
        )

    @patch('smartparams.smart.json.save')
    def test_save__json(self, save: Mock) -> None:
        expected_data = {'class': 'tests.commons.classes.ParentB'}
        path = Path('path/to/file.json')

        self.smart.save(path)

        save.assert_called_with(
            data=expected_data,
            path=path,
        )

    def test_save__unknown_format__value_error(self) -> None:
        self.assertRaises(ValueError, self.smart.save, Path('path/to/file.txt'))

    @patch('smartparams.smart.sys')
    def test_from_cli(self, sys: Mock) -> None:
        expected = {'argument': 10}
        sys.argv = ['script.py', 'argument=10']

        actual = Smart.from_cli()

        self.assertIsInstance(actual, Smart)
        self.assertEqual(expected, actual)

    def test_to_dict(self) -> None:
        expected = {'class': 'tests.commons.classes.ParentB'}

        actual = self.smart.to_dict()

        self.assertIs(type(actual), dict)
        self.assertEqual(expected, actual)

    def test_to_dict__multi_types(self) -> None:
        expected = {'a': ['str', {1: {'a': True}}]}
        smart: Smart = Smart(**expected)

        actual = smart.to_dict()

        self.assertIs(type(actual), dict)
        self.assertEqual(expected, actual)

    def test_to_dict__cannot_create_representation__type_error(self) -> None:
        smart: Smart = Smart(a=Mock())

        self.assertRaises(TypeError, smart.to_dict)

    @patch('smartparams.smart.yaml.to_string')
    def test_to_yaml(self, to_string: Mock) -> None:
        expected = 'class: tests.commons.classes.ParentB\n'
        to_string.return_value = expected

        actual = self.smart.to_yaml()

        self.assertIsInstance(actual, str)
        self.assertEqual(expected, actual)

    @patch('smartparams.smart.json.to_string')
    def test_to_json(self, to_string: Mock) -> None:
        expected = '{\n  "class": "tests.commons.classes.ParentB"\n}'
        to_string.return_value = expected

        actual = self.smart.to_json()

        self.assertIsInstance(actual, str)
        self.assertEqual(expected, actual)

    def test_schema(self) -> None:
        expected = {
            'class': 'tests.commons.classes.ParentB',
            'smart': {},
            'smart_a': {'class': 'tests.commons.classes.ParentA', 'arg1': 'str???', 'arg2': 5},
            'object_a': {'class': 'tests.commons.classes.ParentA', 'arg1': 'str???', 'arg2': 5},
            'type_a': 'tests.commons.classes.ParentA',
            'any_type': '???',
        }

        actual = self.smart.schema()

        self.assertIsInstance(actual, Smart)
        self.assertEqual(expected, actual)

    @patch('smartparams.smart.directory.mkdir')
    def test_mkdir(self, mkdir: Mock) -> None:
        path = Path('path/to/dir')
        version = 'version'
        tz = Mock()
        expected = path / version
        mkdir.return_value = expected

        actual = Smart.mkdir(
            path=path,
            version=version,
            tz=tz,
        )

        self.assertEqual(expected, actual)

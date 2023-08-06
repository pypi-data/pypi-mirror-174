from pathlib import Path
from unittest.mock import Mock, call, patch

from smartparams.utils.imports import autodiscover, import_class
from tests.commons.classes import ParentA, any_type_function
from tests.unit import UnitTest


class TestImportClass(UnitTest):
    def test__class(self) -> None:
        expected = ParentA

        actual = import_class('tests.commons.classes.ParentA')

        self.assertEqual(expected, actual)

    def test__function(self) -> None:
        expected = any_type_function

        actual = import_class('tests.commons.classes.any_type_function')

        self.assertEqual(expected, actual)


class TestAutodiscover(UnitTest):
    @patch('smartparams.utils.imports.importlib')
    def test(self, importlib: Mock) -> None:
        root_dir = Mock(
            rglob=Mock(
                return_value=[
                    Path('/home/path/script.py'),
                    Path('/home/__init__.py'),
                ]
            ),
            is_file=Mock(return_value=False),
            __fspath__=lambda x: '/home',
        )
        expected = [
            Path('path/script.py'),
            Path('__init__.py'),
        ]

        actual = autodiscover(root_dir)

        self.assertEqual(expected, actual)
        root_dir.rglob.assert_called_once_with('*.py')
        importlib.import_module.assert_has_calls(
            [
                call('path.script'),
                call('__init__'),
            ],
        )

    @patch('smartparams.utils.imports.importlib')
    def test__include(self, importlib: Mock) -> None:
        root_dir = Mock(
            rglob=Mock(
                return_value=[
                    Path('/home/path/script.py'),
                    Path('/home/__init__.py'),
                ]
            ),
            is_file=Mock(return_value=False),
            __fspath__=lambda x: '/home',
        )
        expected = [
            Path('path/script.py'),
        ]

        actual = autodiscover(root_dir, include='script')

        self.assertEqual(expected, actual)
        root_dir.rglob.assert_called_once_with('*.py')
        importlib.import_module.assert_has_calls(
            [
                call('path.script'),
            ],
        )

    @patch('smartparams.utils.imports.importlib')
    def test__exclude(self, importlib: Mock) -> None:
        root_dir = Mock(
            rglob=Mock(
                return_value=[
                    Path('/home/path/script.py'),
                    Path('/home/__init__.py'),
                ]
            ),
            is_file=Mock(return_value=False),
            __fspath__=lambda x: '/home',
        )
        expected = [
            Path('__init__.py'),
        ]

        actual = autodiscover(root_dir, exclude='script')

        self.assertEqual(expected, actual)
        root_dir.rglob.assert_called_once_with('*.py')
        importlib.import_module.assert_has_calls(
            [
                call('__init__'),
            ],
        )

    def test__misconfiguration(self) -> None:
        self.assertRaises(ValueError, autodiscover, Path(), include='include', exclude='exclude')

    @patch('smartparams.utils.imports.Log')
    @patch('smartparams.utils.imports.importlib')
    def test__import_error(self, importlib: Mock, log: Mock) -> None:
        data = [
            Path('/home/path/script.py'),
            Path('/home/__init__.py'),
        ]
        expected = [
            Path('path/script.py'),
        ]

        def import_module(module: str) -> None:
            if module == '__init__':
                raise ValueError()

        root_dir = Mock(rglob=Mock(return_value=data), __fspath__=lambda x: '/home')
        importlib.import_module = import_module

        actual = autodiscover(root_dir)

        self.assertEqual(expected, actual)
        log.import_.warning.assert_called_once()

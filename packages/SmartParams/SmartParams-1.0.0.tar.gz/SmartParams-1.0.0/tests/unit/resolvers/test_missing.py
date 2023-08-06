from unittest.mock import Mock, patch

from smartparams import missing_value_resolver
from tests.unit import UnitTest


class TestMissingValueResolver(UnitTest):
    @patch('smartparams.resolvers.missing.Log')
    def test__string(self, log: Mock) -> None:
        register = Mock(missing_value='???')
        name = 'name'
        data = 'data'
        expected = 'data'

        actual = missing_value_resolver(register, name, data)

        self.assertEqual(expected, actual)
        log.init.warning.assert_not_called()

    @patch('smartparams.resolvers.missing.Log')
    def test__missing_value(self, log: Mock) -> None:
        register = Mock(missing_value='???')
        name = 'name'
        data = 'data???'
        expected = 'data???'

        actual = missing_value_resolver(register, name, data)

        self.assertEqual(expected, actual)
        log.init.warning.assert_called_once()

    @patch('smartparams.resolvers.missing.Log')
    def test__any_object(self, log: Mock) -> None:
        register = Mock(missing_value='???')
        name = 'name'
        data = Mock()
        expected = data

        actual = missing_value_resolver(register, name, data)

        self.assertEqual(expected, actual)
        log.init.warning.assert_not_called()

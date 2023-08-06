from smartparams.utils.parser import parse_param
from tests.unit import UnitTest


class TestParamParser(UnitTest):
    def test(self) -> None:
        expected = ('argument', '10')

        actual = parse_param('argument="10"')

        self.assertEqual(expected, actual)

    def test__json_parse(self) -> None:
        expected = ('argument', 10)

        actual = parse_param('argument=10')

        self.assertEqual(expected, actual)

    def test__raw_value(self) -> None:
        expected = ('argument', 'string')

        actual = parse_param('argument=string')

        self.assertEqual(expected, actual)

    def test__no_separator(self) -> None:
        self.assertRaises(ValueError, parse_param, 'argument 10')

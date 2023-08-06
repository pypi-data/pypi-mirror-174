import tempfile
from pathlib import Path

from smartparams.io.yaml import load, save, to_string
from tests.integration import IntegrationTest


class TestYaml(IntegrationTest):
    def setUp(self) -> None:
        self.path = self.FIXTURE_DIR.joinpath('file.yaml')
        self.dict = dict(a=10, b='x', c={'e': True, 'f': False}, d=[1, 2, 3])

    def test_load(self) -> None:
        actual = load(self.path)

        self.assertEqual(self.dict, actual)

    def test_save(self) -> None:
        expected = self.path.read_text()
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir, 'file.yaml')

            save(self.dict, path)

            self.assertEqual(expected, path.read_text())

    def test_to_string(self) -> None:
        expected = self.path.read_text()

        actual = to_string(self.dict)

        self.assertEqual(expected, actual)

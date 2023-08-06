import tempfile
from datetime import datetime, timezone
from pathlib import Path

from smartparams.utils.directory import mkdir
from tests.unit import UnitTest


class TestMkdir(UnitTest):
    def test(self) -> None:
        hour = datetime.now(tz=timezone.utc).hour
        expected = [
            f'001_{hour:02d}_[a-z]+_suffix',
            f'002_{hour:02d}_[a-z]+_suffix',
            f'003_{hour:02d}_[a-z]+_suffix',
        ]
        with tempfile.TemporaryDirectory() as tempdir:
            directory = Path(tempdir, 'folder')

            actual = [
                mkdir(
                    path=directory,
                    version='{num:03}_{H}_{animal}_suffix',
                    tz=timezone.utc,
                )
                for _ in range(3)
            ]

            for act, exp in zip(sorted(actual), expected):
                with self.subTest(exp):
                    self.assertIsInstance(act, Path)
                    self.assertTrue(act.exists())
                    self.assertRegexpMatches(str(act.name), exp)

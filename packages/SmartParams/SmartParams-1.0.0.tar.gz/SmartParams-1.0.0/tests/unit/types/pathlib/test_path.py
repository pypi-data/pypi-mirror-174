from pathlib import Path, PosixPath

from smartparams.types.pathlib.path import class_schema, from_str, simplifier
from tests.unit.types import Types


class TestPath(Types.Test):
    CLS = Path
    DEFAULT = Path('path/to/file.txt')
    CONVERT_VALUES = {
        str: 'path/to/file.txt',
    }

    def init_register(self) -> None:
        self.register(
            cls=Path,
            class_schema=class_schema,
            simplifier=simplifier,
            converter={
                str: from_str,
            },
        )


class TestPosixPath(Types.Test):
    CLS = PosixPath
    DEFAULT = Path('path/to/file.txt')

    def init_register(self) -> None:
        self.register(
            cls=PosixPath,
            class_schema=class_schema,
            simplifier=simplifier,
        )

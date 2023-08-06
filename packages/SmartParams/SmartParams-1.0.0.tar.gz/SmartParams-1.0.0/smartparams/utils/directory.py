import random
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from secrets import token_hex

from smartparams.utils.vocab import VOCABULARY

_PATTERNS = dict(
    num=r'\d+',
    hash=r'[a-f0-9]+',
    h4=r'[a-f0-9]{4}',
    h6=r'[a-f0-9]{6}',
    h8=r'[a-f0-9]{8}',
    uuid=r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',
    adj=r'[a-zA-Z]+',
    noun=r'[a-zA-Z]+',
    animal=r'[a-zA-Z]+',
    Y=r'\d{2,4}',
    m=r'\d{2}',
    d=r'\d{2}',
    H=r'\d{2}',
    M=r'\d{2}',
    S=r'\d{2}',
    f=r'\d+',
)


def mkdir(
    path: Path,
    version: str | None = None,
    tz: timezone | None = None,
) -> Path:
    if version:
        used_values = _get_used_values(
            path=path,
            version=version,
        )
        date = datetime.now(tz=tz)
        version = version.format(
            num=max(map(int, used_values['num']), default=0) + 1,
            hash=token_hex(16),
            h8=token_hex(4),
            h6=token_hex(3),
            h4=token_hex(2),
            uuid=uuid.uuid4(),
            adj=random.choice(VOCABULARY['adjectives']),
            noun=random.choice(VOCABULARY['nouns']),
            animal=random.choice(VOCABULARY['animals']),
            Y=f'{date.year:04d}',
            m=f'{date.month:02d}',
            d=f'{date.day:02d}',
            H=f'{date.hour:02d}',
            M=f'{date.minute:02d}',
            S=f'{date.second:02d}',
            f=f'{date.microsecond:06d}',
        )
        path = path.joinpath(version)

    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_used_values(
    path: Path,
    version: str,
) -> dict[str, list[str]]:
    used_values: dict[str, list[str]] = {key: [] for key in _PATTERNS}

    if not path.exists():
        return used_values

    pattern = _build_pattern(version)
    for sub_path in path.iterdir():
        if sub_path.is_dir() and (match := re.fullmatch(pattern, sub_path.name)):
            for key, value in match.groupdict().items():
                used_values[key].append(value)

    return used_values


def _build_pattern(string: str) -> str:
    offset = 0
    for match in re.finditer(r'{(?P<name>\w+)(?::.+?)?}', string):
        name = match.group('name')
        replacement = rf'(?P<{name}>{_PATTERNS[name]})'
        string = string[: match.start() + offset] + replacement + string[match.end() + offset :]
        offset += len(replacement) - (match.end() - match.start())

    return string

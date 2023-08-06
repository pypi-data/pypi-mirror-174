import unittest
from pathlib import Path


class IntegrationTest(unittest.TestCase):
    FIXTURE_DIR = Path(__file__).parent.joinpath('fixtures')

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsers.csv_parser import CsvReader  # noqa: E402
from parsers.payout_parser import PayoutParser, COLUMN_ALIASES  # noqa: E402


@pytest.fixture
def csv_file_factory(tmp_path):
    def _create(name: str, content: str):
        path = tmp_path / name
        path.write_text(content)
        return str(path)

    return _create


@pytest.fixture
def payout_parser_factory():
    def _factory(reader=None, aliases=None):
        return PayoutParser(reader or CsvReader(), aliases or COLUMN_ALIASES)

    return _factory

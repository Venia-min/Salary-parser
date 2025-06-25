from parsers.utils import normalize_header


COLUMN_ALIASES = {
    "rate": {"hourly_rate", "rate", "salary"},
    "hours": {"hours_worked", "time", "duration"},
}


def test_normalize_known_aliases():
    header = ["name", "hourly_rate", "hours_worked"]
    result = normalize_header(header, COLUMN_ALIASES)
    assert result == ["name", "rate", "hours"]


def test_preserves_non_aliased_columns():
    header = ["name", "email", "department"]
    result = normalize_header(header, COLUMN_ALIASES)
    assert result == ["name", "email", "department"]


def test_mixed_alias_and_original():
    header = ["salary", "hours", "email"]
    result = normalize_header(header, COLUMN_ALIASES)
    assert result == ["rate", "hours", "email"]


def test_case_insensitive():
    header = ["Salary", "Hours_Worked"]
    result = normalize_header(header, COLUMN_ALIASES)
    assert result == ["rate", "hours"]


def test_empty_header():
    header = []
    result = normalize_header(header, COLUMN_ALIASES)
    assert result == []

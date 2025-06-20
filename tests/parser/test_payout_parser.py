from parser.csv_parser import CsvReader
from parser.payout_parser import PayoutParser, COLUMN_ALIASES


def create_temp_csv(tmp_path, filename, content):
    path = tmp_path / filename
    path.write_text(content)
    return str(path)


def parse_with_payout_parser(path: str) -> list[dict]:
    parser = PayoutParser(CsvReader(), COLUMN_ALIASES)
    return parser.parse(path)


def test_parse_valid_file(tmp_path):
    content = "name,salary,hours\nAlice,50,160\nBob,60,150\n"
    path = create_temp_csv(tmp_path, "valid.csv", content)

    result = parse_with_payout_parser(path)

    assert result == [
        {"name": "Alice", "rate": "50", "hours": "160"},
        {"name": "Bob", "rate": "60", "hours": "150"},
    ]


def test_parse_skips_invalid_rows(tmp_path):
    content = "name,salary,hours_worked\nAlice,50\nBob,60,150\n"
    path = create_temp_csv(tmp_path, "invalid.csv", content)

    result = parse_with_payout_parser(path)

    assert len(result) == 1
    assert result[0]["name"] == "Bob"


def test_parse_empty_file(tmp_path):
    path = create_temp_csv(tmp_path, "empty.csv", "")

    result = parse_with_payout_parser(path)

    assert result == []


def test_parse_preserves_non_aliased_columns(tmp_path):
    content = "email,salary,hours\nalice@example.com,40,100\n"
    path = create_temp_csv(tmp_path, "mixed.csv", content)

    result = parse_with_payout_parser(path)

    assert result == [{"email": "alice@example.com", "rate": "40", "hours": "100"}]


def test_load_combines_multiple_files(tmp_path):
    content1 = "name,salary,hours\nAlice,40,100\n"
    content2 = "name,rate,hours_worked\nBob,50,120\n"

    path1 = create_temp_csv(tmp_path, "file1.csv", content1)
    path2 = create_temp_csv(tmp_path, "file2.csv", content2)

    parser = PayoutParser(CsvReader(), COLUMN_ALIASES)
    result = parser.load([path1, path2])

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"

import pytest
from parser.csv_parser import CsvReader


def create_temp_csv(tmp_path, filename, content):
    path = tmp_path / filename
    path.write_text(content)
    return str(path)


def reader_with_csvreader(path: str) -> tuple[list[str], list[list[str]]]:
    reader = CsvReader()
    return reader.read(path)


def test_csvreader_reads_header_and_rows(tmp_path):
    content = "name,age\nAlice,30\nBob,25\n"
    path = create_temp_csv(tmp_path, "test.csv", content)
    header, rows = reader_with_csvreader(path)

    assert header == ["name", "age"]
    assert rows == [["Alice", "30"], ["Bob", "25"]]


def test_csvreader_skips_empty_lines(tmp_path):
    content = "name,age\nAlice,30\n\nBob,25\n"
    path = create_temp_csv(tmp_path, "test.csv", content)
    rows = reader_with_csvreader(path)[1]

    assert len(rows) == 2
    assert rows[1] == ["Bob", "25"]


def test_csvreader_file_not_found():
    reader = CsvReader()
    with pytest.raises(FileNotFoundError):
        reader.read("nonexistent.csv")


def test_csvreader_empty_file(tmp_path):
    content = ""
    path = create_temp_csv(tmp_path, "empty.csv", content)
    header, rows = reader_with_csvreader(path)

    assert header == []
    assert rows == []

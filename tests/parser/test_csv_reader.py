import pytest

from parsers.csv_parser import CsvReader


def reader_with_csvreader(path: str) -> tuple[list[str], list[list[str]]]:
    reader = CsvReader()
    return reader.read(path)


def test_csvreader_reads_header_and_rows(csv_file_factory):
    content = "name,age\nAlice,30\nBob,25\n"
    path = csv_file_factory("test.csv", content)
    header, rows = reader_with_csvreader(path)

    assert header == ["name", "age"]
    assert rows == [["Alice", "30"], ["Bob", "25"]]


def test_csvreader_skips_empty_lines(csv_file_factory):
    content = "name,age\nAlice,30\n\nBob,25\n"
    path = csv_file_factory("test.csv", content)
    rows = reader_with_csvreader(path)[1]

    assert len(rows) == 2
    assert rows[1] == ["Bob", "25"]


def test_csvreader_file_not_found():
    reader = CsvReader()
    with pytest.raises(FileNotFoundError):
        reader.read("nonexistent.csv")


def test_csvreader_empty_file(csv_file_factory):
    content = ""
    path = csv_file_factory("empty.csv", content)
    header, rows = reader_with_csvreader(path)

    assert header == []
    assert rows == []

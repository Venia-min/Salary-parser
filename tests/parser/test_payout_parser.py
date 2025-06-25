from models.employee import Employee


def test_parse_valid_file(csv_file_factory, payout_parser_factory):
    content = "name,department,salary,hours\nAlice,Design,50,160\nBob,Design,60,150\n"
    path = csv_file_factory("valid.csv", content)

    result = payout_parser_factory().parse(path)

    assert result == [
        Employee(name="Alice", department="Design", rate=50.0, hours=160.0),
        Employee(name="Bob", department="Design", rate=60.0, hours=150.0),
    ]


def test_parse_skips_invalid_rows(csv_file_factory, payout_parser_factory):
    content = "name,department,salary,hours\nAlice,Design,160\nBob,Design,60,150\n"
    path = csv_file_factory("invalid.csv", content)

    result = payout_parser_factory().parse(path)

    assert len(result) == 1
    assert result[0].name == "Bob"


def test_parse_empty_file(csv_file_factory, payout_parser_factory):
    path = csv_file_factory("empty.csv", "")

    result = payout_parser_factory().parse(path)

    assert result == []


def test_parse_preserves_non_aliased_columns(csv_file_factory, payout_parser_factory):
    content = (
        "name,email,salary,hours,department\nAlice,alice@example.com,40,100,Design\n"
    )
    path = csv_file_factory("mixed.csv", content)

    result = payout_parser_factory().parse(path)

    assert len(result) == 1
    employee = result[0]
    assert isinstance(employee, Employee)
    assert employee.name == "Alice"
    assert employee.rate == 40.0
    assert employee.hours == 100.0
    assert employee.department == "Design"


def test_load_combines_multiple_files(csv_file_factory, payout_parser_factory):
    content1 = "name,salary,hours,department\nAlice,40,100,Design\n"
    content2 = "name,rate,hours_worked,department\nBob,50,120,Marketing\n"

    path1 = csv_file_factory("file1.csv", content1)
    path2 = csv_file_factory("file2.csv", content2)

    result = payout_parser_factory().load([path1, path2])

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[0].rate == 40.0
    assert result[0].hours == 100.0
    assert result[0].department == "Design"

    assert result[1].name == "Bob"
    assert result[1].rate == 50.0
    assert result[1].hours == 120.0
    assert result[1].department == "Marketing"

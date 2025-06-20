from reports.payout import PayoutReport


def report_format(raw_data):
    report = PayoutReport(files=[])
    report.raw_data = raw_data
    report.format()
    return report.report_data


def test_format_single_entry():
    raw_data = [{"department": "Design", "name": "Alice", "rate": "50", "hours": "160"}]

    report_data = report_format(raw_data)

    assert "Design" in report_data
    dept = report_data["Design"]
    assert dept["total_hours"] == 160.0
    assert dept["total_payout"] == 8000.0
    assert dept["employees"] == [
        {
            "department": "Design",
            "name": "Alice",
            "hours": 160.0,
            "rate": 50.0,
            "payout": 8000.0,
        }
    ]


def test_format_multiple_departments():
    raw_data = [
        {"department": "Design", "name": "Bob", "rate": "40", "hours": "150"},
        {"department": "Marketing", "name": "Alice", "rate": "60", "hours": "100"},
    ]

    report_data = report_format(raw_data)

    assert set(report_data.keys()) == {"Design", "Marketing"}
    assert report_data["Design"]["total_payout"] == 6000.0
    assert report_data["Marketing"]["total_payout"] == 6000.0


def test_format_skips_invalid_entries():
    raw_data = [
        {"department": "Design", "name": "Eve", "rate": "not_a_number", "hours": "150"},
        {"department": "Design", "name": "Eve", "rate": "40", "hours": "invalid"},
        {"department": "Design", "name": "Eve", "rate": "40", "hours": "150"},
    ]

    report_data = report_format(raw_data)

    assert len(report_data["Design"]["employees"]) == 1
    assert report_data["Design"]["total_payout"] == 6000.0


def test_format_empty_raw_data():
    raw_data = []
    report_data = report_format(raw_data)
    assert report_data == {}


def test_print_empty_report(capsys):
    report = PayoutReport(files=[])
    report.report_data = {}  # явно пусто

    report.print()
    captured = capsys.readouterr()

    assert "Отчет пуст." in captured.out

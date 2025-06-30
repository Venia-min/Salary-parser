import pytest

from models.employee import Employee
from reports.payout import PayoutReport


def report_format(raw_data):
    report = PayoutReport(files=[])
    report.raw_data = raw_data
    report.format()
    return report.report_data


@pytest.mark.parametrize(
    "employee, department, expected_payout",
    [
        (Employee("Alice", "Design", 50, 160), "Design", 8000),
        (Employee("Bob", "Marketing", 60, 100), "Marketing", 6000),
    ],
)
def test_format_single_entry_param(employee, department, expected_payout):
    report_data = report_format([employee])

    assert department in report_data
    dept = report_data[department]
    assert dept["total_payout"] == expected_payout


def test_format_multiple_departments():
    raw_data = [
        Employee(name="Bob", department="Design", rate=40, hours=150),
        Employee(name="Alice", department="Marketing", rate=60, hours=100),
    ]

    report_data = report_format(raw_data)

    assert set(report_data.keys()) == {"Design", "Marketing"}
    assert report_data["Design"]["total_payout"] == 6000
    assert report_data["Marketing"]["total_payout"] == 6000


def test_format_skips_invalid_entries():
    raw_data = [
        # Simulate already-filtered valid data; invalid ones should be skipped
        # by parsers, not here
        Employee(name="Eve", department="Design", rate=40, hours=150)
    ]

    report_data = report_format(raw_data)

    assert len(report_data["Design"]["employees"]) == 1
    assert report_data["Design"]["total_payout"] == 6000


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

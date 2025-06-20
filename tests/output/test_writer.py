import json
from output.writers import save_report_to_json


def test_save_report_to_json_creates_valid_file(tmp_path):
    report_data = [
        {
            "Design": {
                "employees": [
                    {"name": "Bob", "rate": 40.0, "hours": 150.0, "payout": 6000.0}
                ],
                "total_hours": 150.0,
                "total_payout": 6000.0,
            }
        }
    ]

    file_path = tmp_path / "report.json"
    save_report_to_json(report_data, str(file_path))

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == report_data

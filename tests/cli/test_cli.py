import json
import os
import subprocess
import sys


def test_cli_console_output(csv_file_factory):
    csv_content = "name,salary,hours_worked,department\nAlice,50,160,Design\n"
    csv_path = csv_file_factory("input.csv", csv_content)

    result = subprocess.run(
        [sys.executable, "main.py", csv_path, "--report", "payout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd(),
    )

    assert result.returncode == 0
    assert "Design" in result.stdout
    assert "Alice" in result.stdout
    assert "$8000" in result.stdout


def test_cli_json_output(csv_file_factory, tmp_path):
    csv_content = "name,salary,hours_worked,department\nBob,60,100,Marketing\n"
    csv_path = csv_file_factory("input.csv", csv_content)
    output_path = tmp_path / "output"

    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            csv_path,
            "--report",
            "payout",
            "--output",
            "json",
            "--output-path",
            str(output_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd(),
    )

    expected_file = tmp_path / "output.json"
    assert result.returncode == 0
    assert expected_file.exists()

    with open(expected_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "Marketing" in data
    assert data["Marketing"]["total_payout"] == 6000.0

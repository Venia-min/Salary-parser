import json


def save_report_to_json(report: list[dict], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


ALLOWED_SAVE_FUNCTIONS = {
    "json": save_report_to_json,
}
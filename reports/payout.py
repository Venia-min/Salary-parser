from pathlib import Path

from output.writers import ALLOWED_SAVE_FUNCTIONS
from parser.csv_parser import parse_and_combine


def format_report(data: list[dict]) -> list[dict]:
    """
    Форматирует данные для отчета payout.
    :param data: Данные для форматирования
    :return: Отформатированные данные
    """
    result = []
    for row in data:
        try:
            hours = float(row.get("hours_worked", 0))
            rate = float(row.get("rate", 0))
            payout = round(hours * rate, 2)
        except (ValueError, TypeError):
            continue

        result.append({
            "department": row.get("department", "Unknown"),
            "name": row.get("name", "Unknown"),
            "hours": hours,
            "rate": rate,
            "payout": payout
        })

    return result


def print_report(report: list[dict]) -> None:
    """
    Печатает отчет в консоль в структурированном виде.
    :param report: Отчет для печати
    :return: None
    """
    total_hours = 0
    total_payout = 0
    print("\n Payout Report:")
    print(f"\n {report[0].keys()[0]:<10}{report[0].keys()[1]:<20}{report[0].keys()[2]:>10}{report[0].keys()[3]:>10}{report[0].keys()[4]:>10}")
    for line in report:
        print(
            f"{'':<4}{'-' * 16:<4}{line['name']:<20}{int(line['hours']):>6}{int(line['rate']):>7}   ${int(line['payout']):>6}"
        )
        total_hours += line["hours"]
        total_payout += line["payout"]
        print(f"{'':<30}{int(total_hours):>6}{'':>7}   ${int(total_payout):>6}")
        print()


def generate(
        files: list[str],
        output_format: str = "console",
        output_path: str = "report_payout"
) -> None:
    """
    Генерирует отчет и выводит его в консоль или сохраняет в файл.
    :param files: Список путей к файлам
    :param output_format: формат вывода
    :param output_path: путь к файлу для сохранения
    :return: None
    """
    data = parse_and_combine(files)
    report = format_report(data)

    if output_format == "console":
        print_report(report)
    elif output_format in ALLOWED_SAVE_FUNCTIONS:
        full_path = str(
            Path(output_path).with_suffix(f".{output_format}")
        )
        ALLOWED_SAVE_FUNCTIONS[output_format](report, full_path)
    else:
        raise ValueError(f"Недоступный формат вывода: {output_format}")

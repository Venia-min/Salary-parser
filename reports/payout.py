from collections import defaultdict
from pathlib import Path

from models.employee import Employee
from output import SAVE_VARIANTS
from parsers.csv_parser import CsvReader
from parsers.payout_parser import PayoutParser, COLUMN_ALIASES


class PayoutReport:
    def __init__(self, files: list[str]):
        self.files = files
        self.parser = PayoutParser(CsvReader(), COLUMN_ALIASES)
        self.raw_data: list[Employee] = []
        self.report_data: dict[str, dict] = {}

    def load(self) -> None:
        """
        Загружает данные из файлов.
        """
        self.raw_data = self.parser.load(self.files)

    def format(self) -> None:
        """
        Форматирует данные для отчета payout.
        """
        grouped_data = defaultdict(
            lambda: {"employees": [], "total_hours": 0, "total_payout": 0}
        )
        for emp in self.raw_data:
            dept = emp.department
            grouped_data[dept]["employees"].append(
                {
                    "name": emp.name,
                    "hours": emp.hours,
                    "rate": emp.rate,
                    "payout": emp.payout,
                }
            )
            grouped_data[dept]["total_hours"] += emp.hours
            grouped_data[dept]["total_payout"] += emp.payout

        self.report_data = dict(grouped_data)

    def print(self) -> None:
        """
        Печатает отчет в консоль в структурированном виде.
        """
        if not self.report_data:
            print("Отчет пуст.")
            return

        print("\nPayout Report:")
        print(f"{'':<16}{'name':<20}{'hours':<8}{'rate':<7}{'payout':<7}\n")

        for department, data in self.report_data.items():
            print(f"{department}")
            total_hours = int(data["total_hours"])
            total_payout = int(data["total_payout"])

            for employee in data["employees"]:
                name = employee["name"]
                hours = int(employee["hours"])
                rate = int(employee["rate"])
                payout = int(employee["payout"])
                print(f"{'-' * 15:<4} {name:<20}{hours:<8}{rate:<7}${payout:<6}")

            # Суммы по отделу
            print(f"{'':<36}{total_hours:<7}{'':>8}${total_payout:<6}\n")

    def save(self, output_format: str, output_path: str) -> None:
        """
        Сохраняет отчет в указанном формате.
        :param output_format: Формат вывода отчета
        :param output_path: Путь к файлу для сохранения
        """
        path = str(Path(output_path).with_suffix(f".{output_format}"))
        SAVE_VARIANTS[output_format](self.report_data, path)

    def generate(
        self, output_format: str = "console", output_path: str = "data/report_payout"
    ) -> None:
        """
        Генерирует отчет и выводит его в консоль или сохраняет в файл.
        :param output_format: Формат вывода отчета
        :param output_path: Путь к файлу для сохранения
        """
        self.load()
        self.format()

        if output_format == "console":
            self.print()
        else:
            self.save(output_format, output_path)

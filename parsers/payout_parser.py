from models.employee import Employee
from parsers.utils import normalize_header


# Наименования полей у которых есть синонимы
COLUMN_ALIASES = {
    "rate": {"hourly_rate", "rate", "salary"},
    "hours": {"hours_worked"},
}


class PayoutParser:
    def __init__(self, reader, column_aliases):
        self.reader = reader
        self.column_aliases = column_aliases

    def parse(self, file_path: str) -> list[Employee]:
        """
        Читает CSV-файл с помощью переданного reader, нормализует заголовки,
        фильтрует строки с неправильным количеством значений.
        :param file_path: Путь к файлу
        :return: Список словарей с нормализованными ключами
        """
        header, rows = self.reader.read(file_path)
        if not header:
            return []

        normalized_header = normalize_header(header, self.column_aliases)
        data = []

        for values in rows:
            if len(values) != len(normalized_header):
                print(
                    f"Ошибка: неверное количество столбцов в строке: {values}."
                    f"Ожидается {len(normalized_header)}, получено {len(values)}"
                )
                continue

            row = dict(zip(normalized_header, values))
            try:
                employee = Employee(
                    name=row["name"],
                    department=row["department"],
                    rate=float(row["rate"]),
                    hours=float(row["hours"]),
                )
                data.append(employee)
            except (KeyError, ValueError) as e:
                print(f"Ошибка при обработке строки: {values}. Ошибка: {e}")

        return data

    def load(
        self,
        files: list[str],
    ) -> list[dict]:
        """
        Обрабатывает список файлов и объединяет результаты.
        :param files: Список путей к файлам
        :return: Объединенные данные из всех файлов
        """
        combined_data = []
        for file_path in files:
            data = self.parse(file_path)
            combined_data.extend(data)
        return combined_data

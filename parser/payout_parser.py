from parser.csv_parser import CsvReader
from parser.utils import normalize_header


# Наименования полей у которых есть синонимы
COLUMN_ALIASES = {
    'rate': {'hourly_rate', 'rate', 'salary'},
}


class PayoutParser:
    def __init__(self, reader, column_aliases):
        self.reader = reader
        self.column_aliases = column_aliases

    def parse(self, file_path: str) -> list[dict]:
        """
        Читает CSV-файл с помощью переданного reader, нормализует заголовки,
        фильтрует строки с неправильным количеством значений,
        возвращает список словарей с нормализованными ключами.
        :param file_path: Путь к файлу
        """
        header, rows = self.reader.read(file_path)
        if not header:
            return []

        normalized_header = normalize_header(header, self.column_aliases)
        data = []

        for values in rows:
            if len(values) != len(normalized_header):
                print(f"Ошибка: неверное количество столбцов в строке: {values}."
                      f"Ожидается {len(normalized_header)}, получено {len(values)}")
                continue

            row = dict(zip(normalized_header, values))
            data.append(row)

        return data

    def load(
            self,
            files: list[str],
    ) -> list[dict]:
        """
        Обрабатывает список файлов с помощью PayoutCsvParser и объединяет результаты.
        :param files: Список путей к файлам
        :return: Объединенные данные из всех файлов
        """
        combined_data = []
        for file_path in files:
            data = self.parse(file_path)
            combined_data.extend(data)
        return combined_data



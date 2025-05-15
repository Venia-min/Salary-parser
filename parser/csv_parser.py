import os
from typing import List, Dict


# Наименования полей у которых есть синонимы
COLUMN_ALIASES = {
    'rate': {'hourly_rate', 'rate', 'salary'},
}

def normalize_header(header, column_aliases) -> List[str]:
    """
    Заменяет заголовки CSV по известным синонимам.
    Остальные оставляет без изменений.
    :param header: Заголовки столбцов
    :param column_aliases: Синонимы наименований столбцов
    """
    normalized_header = header[:]
    for i, column in enumerate(header):
        column = column.lower()
        for standard_name, aliases in column_aliases.items():
            if column in aliases:
                normalized_header[i] = standard_name
                break
    return normalized_header


def read_csv_file(file_path: str) -> List[Dict[str, str]]:
    """
    Читает CSV-файл, нормализует заголовки и возвращает список словарей.
    :param file_path: Путь к файлу
    :return: Список словарей с данными
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        return []

    header = lines[0].strip().split(",")
    normalized_header = normalize_header(header, COLUMN_ALIASES)

    data = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        values = [v.strip() for v in line.split(',')]
        if len(values) != len(normalized_header):
            print(f"Ошибка: неверное количество столбцов в строке: {line}."
                  f"Ожидается {len(normalized_header)}, получено {len(values)}")
            continue

        row = dict(zip(normalized_header, values))
        data.append(row)

    return data


def parse_and_combine(files: list[str]) -> list[dict]:
    """
    Читает CSV-файлы и объединяет их данные.
    :param files: Список путей к файлам
    :return: Объединенные данные
    """
    combined_data = []
    for file_path in files:
        data = read_csv_file(file_path)
        combined_data.extend(data)
    return combined_data
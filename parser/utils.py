from typing import List


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

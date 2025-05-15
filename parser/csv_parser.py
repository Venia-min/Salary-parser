import os

class CsvReader:
    """
    Базовый класс для чтения CSV-файлов.
    """
    def read(self, file_path: str) -> tuple[list[str], list[list[str]]]:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not lines:
            return [], []

        header = lines[0].strip().split(",")
        rows = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            values = [v.strip() for v in line.split(',')]
            rows.append(values)

        return header, rows

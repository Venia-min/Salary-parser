# Salary Report CLI Utility

Утилита для чтения данных сотрудников из CSV-файлов и формирования отчётов по заработной плате (payout) с возможностью расширения на другие типы отчётов.

## 🚀 Быстрый старт

### Установка

Скачайте проект из GitHub:

```bash
git clone https://github.com/venia-min/salary-report.git
cd salary-report
```

Установте зависимости:
```bash
pip install -r requirements.txt
```

### Запуск
```bash
python main.py data1.csv data2.csv --report payout
```
По умолчанию отчёт выводится в консоль.

### Сохранение отчёта в JSON
```bash
python main.py data1.csv --report payout --output json --output-path data/default_report
```
Если --output-path не указан, используется стандартный путь:
data/default_report.json (для JSON).

## 📝 Пример вывода отчёта

<img width="471" alt="Screenshot 2025-05-16 at 2 38 28 AM" src="https://github.com/user-attachments/assets/41241988-ffe9-4f10-ae43-fb95da7bbd7b" />

## 🧩 Структура проекта
  
  -	parser/ - универсальный CSV-парсер и специфичные парсеры отчётов
  -	reports/ - классы отчётов с методами агрегации и форматирования
  -	output/ - функции сохранения отчётов в разных форматах
  -	tests/ - тесты проекта

## ➕ Как добавить новый отчёт
1. Создайте класс отчёта в папке reports/, например NewReport.
  - Обязателен метод generate() - он отвечает за генерацию отчёта и вывод/сохранение результата.
  - Методы load(), format(), print(), save() - опциональны, можно реализовать по необходимости.
2. Создайте парсер для обработки CSV (можно использовать CsvReader из parser/).
  - Парсер должен считывать и нормализовать данные под требования отчёта.
3. Зарегистрируйте отчёт в reports/__init__.py:
```python
from .new_report import NewReport

REPORT_VARIANTS = {
    "payout": ReportPayout,
    "newreport": NewReport,
}
```

4. Добавьте новый метод сохранения (если требуется):
  - Реализуйте функцию сохранения в output/writers.py, например save_report_to_xml(report, path).
  - Зарегистрируйте функцию в output/__init__.py:
```python
SAVE_VARIANTS = {
"json": save_report_to_json,
"xml": save_report_to_xml,
}
```

## 🔑 Важно

- Ключи в словарях REPORT_CLASSES и SAVE_VARIANTS — это значения, которые используются в CLI-параметрах --report и --output.
- При добавлении новых отчётов или форматов сохранения — обязательно обновляйте эти словари для поддержки CLI.

## 🧪 Тестирование

  Запуск всех тестов с отчётом о покрытии:
  ```bash
  pytest --cov=.
  ```




 

from .payout import PayoutReport


# Словарь доступных типов отчётов.
# Ключ — имя отчёта, передаваемое через аргумент --report.
# Значение — класс, реализующий метод .generate(...).
# При добавлении нового отчёта нужно добавить его в словарь.
REPORT_VARIANTS = {
    "payout": PayoutReport,
}


def get_report_class(report_name: str):
    """
    Возвращает класс отчета по его названию.
    :param report_name: Название отчета
    :return: Класс отчета или None, если отчет не найден
    """
    return REPORT_VARIANTS.get(report_name)

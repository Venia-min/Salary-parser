import argparse
from pathlib import Path

from output import SAVE_VARIANTS
from reports import get_report_class, REPORT_VARIANTS


def existing_file(path_str: str) -> Path:
    path = Path(path_str)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"Файл не найден: {path}")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Генерация отчета")

    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        type=existing_file,
        help="Путь к одному или нескольким файлам с данными",
    )

    parser.add_argument(
        "--report",
        required=True,
        choices=REPORT_VARIANTS.keys(),
        help=f"Тип отчета для генерации. Обязательный аргумент. "
        f"Варианты: {REPORT_VARIANTS.keys()}",
    )

    parser.add_argument(
        "--output",
        default="console",
        choices=SAVE_VARIANTS.keys(),
        help=f"Опционально: формат вывода отчета. "
        f"По умолчанию: вывод в консоль. "
        f"Варианты: {SAVE_VARIANTS.keys()}",
    )

    parser.add_argument(
        "--output-path",
        default="data/report_default",
        help="Путь для сохранения отчета",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    report_class = get_report_class(args.report)

    report = report_class(files=args.files)
    report.generate(output_format=args.output, output_path=args.output_path)


if __name__ == "__main__":
    main()

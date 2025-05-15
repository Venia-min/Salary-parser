import argparse
import sys
from reports import get_report_class


ALLOWED_REPORTS = ["payout"]
ALLOWED_FORMATS = ["json"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Генерация отчета"
    )

    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="Путь к одному или нескольким файлам с информацией",
    )

    parser.add_argument(
        "--report",
        required=True,
        choices=ALLOWED_REPORTS,
        help=f"Тип отчета для генерации. Варианты: {ALLOWED_REPORTS}",
    )

    parser.add_argument(
        "--output",
        default="console",
        choices=ALLOWED_FORMATS,
        help=f"Опционально: формат вывода отчета. Варианты:  {ALLOWED_FORMATS}",
    )

    parser.add_argument(
        "--output-path",
        default="report_default.json",
        help="Путь для сохранения отчета",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    report_class = get_report_class(args.report)
    if not report_class:
        print(f"Неизвестный тип отчета: {args.report}", file=sys.stderr)
        sys.exit(1)

    report = report_class()
    report.generate(args.files, args.output, args.output_path)


if __name__ == "__main__":
    main()
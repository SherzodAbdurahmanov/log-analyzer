import argparse
import os
import sys
from parser.log_parser import parse_log_file
from reports.handlers import generate_report

# Словарь доступных отчётов: легко добавить новые, просто подключив функцию
AVAILABLE_REPORTS = {
    "handlers": generate_report,
}


def validate_files(filepaths: list[str]) -> list[str]:
    """
    Проверяет существование переданных файлов.
    Завершает выполнение, если хотя бы одного файла нет.
    """
    for path in filepaths:
        if not os.path.exists(path):
            print(f"Файл не найден: {path}")
            sys.exit(1)
    return filepaths


def main():
    """
    Основная точка входа CLI-приложения.
    Читает аргументы, валидирует их и вызывает нужный отчёт.
    """
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("logfiles", nargs="+", help="Пути к лог-файлам")
    parser.add_argument("--report", required=True, help="Тип отчета")

    args = parser.parse_args()

    # Проверяем, что отчёт с таким именем существует
    report_name = args.report
    if report_name not in AVAILABLE_REPORTS:
        print(f"Неверное имя отчёта: {report_name}")
        print(f"Доступные отчёты: {', '.join(AVAILABLE_REPORTS.keys())}")
        sys.exit(1)

    # Проверка существования файлов
    validate_files(args.logfiles)

    # Объединяем статистику по всем логам
    combined_stats = {}
    for filepath in args.logfiles:
        file_stats = parse_log_file(filepath)
        for handler, levels in file_stats.items():
            if handler not in combined_stats:
                combined_stats[handler] = {}
            for level, count in levels.items():
                combined_stats[handler][level] = combined_stats[handler].get(level, 0) + count

    # Вызываем нужный отчёт
    report_func = AVAILABLE_REPORTS[report_name]
    report_func(combined_stats)


if __name__ == "__main__":
    main()

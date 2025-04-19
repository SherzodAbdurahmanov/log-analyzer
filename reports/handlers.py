from typing import Dict

# Уровни логирования, которые учитываются в отчёте
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def generate_report(stats: Dict[str, Dict[str, int]]) -> None:
    """
    Формирует табличный отчёт по ручкам и уровням логирования.
    Сортирует ручки по алфавиту и выводит общую сумму по уровням.
    """
    # Общее количество запросов
    print("Total requests:", sum(
        sum(levels.values()) for levels in stats.values()
    ))

    print()  # пустая строка

    # Заголовок таблицы
    header = "HANDLER".ljust(25) + "".join(level.ljust(10) for level in LOG_LEVELS)
    print(header)

    # Строки отчёта по каждой ручке
    for handler in sorted(stats.keys()):
        row = handler.ljust(25)
        for level in LOG_LEVELS:
            count = stats[handler].get(level, 0)
            row += str(count).ljust(10)
        print(row)

    # Итоговая строка со всеми суммами по колонкам
    total_by_level = {level: 0 for level in LOG_LEVELS}
    for handler_stats in stats.values():
        for level in LOG_LEVELS:
            total_by_level[level] += handler_stats.get(level, 0)

    footer = "".ljust(25) + "".join(str(total_by_level[level]).ljust(10) for level in LOG_LEVELS)
    print(footer)

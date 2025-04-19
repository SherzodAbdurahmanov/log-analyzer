from typing import Dict

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def generate_report(stats: Dict[str, Dict[str, int]]) -> None:
    print("Total requests:", sum(
        sum(levels.values()) for levels in stats.values()
    ))

    print()  # пустая строка

    # Печатаем заголовки
    header = "HANDLER".ljust(25) + "".join(level.ljust(10) for level in LOG_LEVELS)
    print(header)

    # Печатаем строки по каждому handler'у
    for handler in sorted(stats.keys()):
        row = handler.ljust(25)
        for level in LOG_LEVELS:
            count = stats[handler].get(level, 0)
            row += str(count).ljust(10)
        print(row)

    # Подсчитываем общий итог по колонкам
    total_by_level = {level: 0 for level in LOG_LEVELS}
    for handler_stats in stats.values():
        for level in LOG_LEVELS:
            total_by_level[level] += handler_stats.get(level, 0)

    # Печатаем итоговую строку
    footer = "".ljust(25) + "".join(str(total_by_level[level]).ljust(10) for level in LOG_LEVELS)
    print(footer)

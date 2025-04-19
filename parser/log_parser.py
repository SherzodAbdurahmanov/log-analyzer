import re
from collections import defaultdict
from typing import Dict


def parse_log_line(line: str) -> dict | None:
    """
    Парсит одну строку лога и извлекает уровень логирования и путь к ручке,
    если это строка от django.request. Возвращает None, если строка нерелевантна.

    Примеры поддерживаемых строк:
    - 2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK
    - 2025-03-28 12:07:59,000 ERROR django.request: Internal Server Error: /api/v1/support/ [...]
    """
    if "django.request" not in line:
        return None

    # Шаблон 1: обычный запрос (GET /... 200 OK)
    pattern1 = r"^\S+ \S+ (?P<level>\w+) django\.request: \w+ (?P<handler>/\S+)"

    # Шаблон 2: ошибки, где путь к ручке идёт после двоеточия
    pattern2 = r"^\S+ \S+ (?P<level>\w+) django\.request: .*?: (?P<handler>/\S+)"

    match = re.search(pattern1, line)
    if not match:
        match = re.search(pattern2, line)

    if match:
        return {
            "level": match.group("level").upper(),
            "handler": match.group("handler")
        }

    return None


def parse_log_file(filepath: str) -> Dict[str, Dict[str, int]]:
    """
    Обрабатывает лог-файл построчно и возвращает статистику:
    handler -> log_level -> count

    Построчное чтение позволяет обрабатывать большие файлы (гигабайты данных)
    без загрузки всего файла в память.
    """
    stats = defaultdict(lambda: defaultdict(int))
    with open(filepath, 'r') as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                handler = result["handler"]
                level = result["level"]
                stats[handler][level] += 1

    return stats

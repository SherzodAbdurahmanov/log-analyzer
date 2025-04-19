import re
from collections import defaultdict
from typing import Dict


def parse_log_line(line: str) -> dict | None:
    if "django.request" not in line:
        return None

    pattern1 = r"^\S+ \S+ (?P<level>\w+) django\.request: \w+ (?P<handler>/\S+)"
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
    stats = defaultdict(lambda: defaultdict(int))
    with open(filepath, 'r') as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                handler = result["handler"]
                level = result["level"]
                stats[handler][level] += 1

    return stats

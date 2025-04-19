from parser.log_parser import parse_log_line, parse_log_file


def test_parse_get_line():
    line = "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK"
    result = parse_log_line(line)
    assert result == {
        "level": "INFO",
        "handler": "/api/v1/reviews/"
    }


def test_parse_error_line():
    line = "2025-03-28 12:07:59,000 ERROR django.request: Internal Server Error: /api/v1/support/ [192.168.1.45]"
    result = parse_log_line(line)
    assert result == {
        "level": "ERROR",
        "handler": "/api/v1/support/"
    }


def test_ignore_non_request_line():
    line = "2025-03-28 12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;"
    result = parse_log_line(line)
    assert result is None


def test_parse_log_file(tmp_path):
    log_text = """\
2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK
2025-03-28 12:07:59,000 ERROR django.request: Internal Server Error: /api/v1/support/
2025-03-28 12:03:09,000 DEBUG django.db.backends: SELECT * FROM users;
"""
    log_file = tmp_path / "test.log"
    log_file.write_text(log_text)

    result = parse_log_file(str(log_file))

    assert result == {
        "/api/v1/reviews/": {"INFO": 1},
        "/api/v1/support/": {"ERROR": 1}
    }

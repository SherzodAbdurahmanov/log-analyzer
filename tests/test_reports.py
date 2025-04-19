from reports.handlers import generate_report


def test_generate_report_output(capsys):
    stats = {
        "/api/v1/reviews/": {"INFO": 3, "ERROR": 1},
        "/api/v1/orders/": {"DEBUG": 2, "INFO": 5, "ERROR": 2}
    }

    generate_report(stats)

    captured = capsys.readouterr()
    output = captured.out

    assert "Total requests: 13" in output
    assert "/api/v1/orders/" in output
    assert "/api/v1/reviews/" in output
    assert "DEBUG" in output
    assert "ERROR" in output

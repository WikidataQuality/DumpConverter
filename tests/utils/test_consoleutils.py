"""Contains test for consoleutils package"""
import pytest

from dumpconverter.utils import consoleutils


@pytest.mark.parametrize(["message", "current_bytes", "total_bytes", "expected_output"], [
    (
        "Progress...{0}",
        512,
        None,
        "Progress...512.0 B"
    ),
    (
        "Progress...{0}",
        1024,
        2048,
        "Progress...50.0%"
    ),
    (
        "Progress...",
        1024,
        2048,
        "Progress..."
    )
])
def test_print_progress(message, current_bytes, total_bytes, expected_output, capsys):
    consoleutils.print_progress(message, current_bytes, total_bytes)
    out, err = capsys.readouterr()

    assert "\r\x1b[K" + expected_output == str(out)


@pytest.mark.parametrize(["bytes_count", "precision", "expected_output"], [
    (
        0,
        2,
        "0 B"
    ),
    (
        42,
        2,
        "42.0 B"
    ),
    (
        1248,
        2,
        "1.22 KB"
    ),
    (
        2345000,
        3,
        "2.236 MB"
    ),
    (
        1678500000,
        4,
        "1.5632 GB"
    ),
    (
        1099511627776,
        2,
        "1.0 TB"
    ),
    (
        1125899906842624,
        2,
        "1.0 PB"
    ),
    (
        1152921504606846976,
        2,
        "1.0 EB"
    ),
    (
        1180591620717411303424,
        2,
        "1.0 ZB"
    )
])
def test_format_bytes(bytes_count, precision, expected_output):
    actual_output = consoleutils.format_bytes(bytes_count, precision)

    assert expected_output == actual_output
import pytest
import unittest

from io import BytesIO

from dumpconverter.exceptions import DownloadError
from dumpconverter.DumpConverter import DumpConverter


def test_download_dump_success():
    # Create converter
    dump_converter = create_dump_converter()

    # Download test page that returns 200
    url = "http://httpstat.us/200"
    downloaded_file = dump_converter.download_dump(url)

    # Run assertions
    assert 0 == downloaded_file.tell()
    assert dump_converter.data_source_size == get_file_size(downloaded_file)
    assert "200 OK" == downloaded_file.read()


@pytest.mark.parametrize("url", [
    "http://httpstat.us/204",
    "http://httpstat.us/404",
    "http://httpstat.us/418"
])
def test_download_dump_error(url):
    with pytest.raises(DownloadError.DownloadError):
        dump_converter = create_dump_converter()
        dump_converter.download_dump(url)


@pytest.mark.parametrize(["message", "read_bytes", "total_bytes", "expected_output"], [
    (
        "Progress...{0}",
        512,
        -1,
        "Progress...512.0 B\r"
    ),
    (
        "Progress...{0}",
        1024,
        2048,
        "Progress...50.0%\r"
    ),
    (
        "Progress...",
        1024,
        2048,
        "Progress...\r"
    )
])
def test_print_progress(message, read_bytes, total_bytes, expected_output, capsys):
    DumpConverter.print_progress(message, read_bytes, total_bytes)

    out, err = capsys.readouterr()
    assert expected_output == str(out)


@pytest.mark.parametrize(["bytes", "precision", "expected_output"], [
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
def test_format_bytes(bytes, precision, expected_output):
    actual_output = DumpConverter.format_bytes(bytes, precision)
    assert expected_output == actual_output


@pytest.mark.parametrize(["formatter", "nodes", "expected_result"], [
    (
        "nodes[0].split('-')[0]",
        ["01.01.2015-31.12.2015"],
        "01.01.2015"
    ),
    (
        "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]",
        ["Adams, Douglas"],
        "Douglas Adams"
    ),
    (
        "nodes[0] + nodes[1]",
        ["foo", "bar"],
        "foobar"
    ),
    (
        "nodes[1]",
        ["foobar"],
        None
    )
])
def test_run_formatter(formatter, nodes, expected_result):
    actual_result = DumpConverter.run_formatter(formatter, nodes)
    assert actual_result == expected_result


@pytest.mark.parametrize(["identifier_pid", "external_id", "pid", "value"], [
    (
        227,
        "foobar42",
        31,
        "foobar"
    )
])
def test_write_entities_csv_row(identifier_pid, external_id, pid, value):
    # Create file-like strings for csv output
    csv_entities_file = BytesIO()
    csv_meta_file = BytesIO()

    # Create dump converter and write csv
    dump_converter = create_dump_converter(csv_entities_file, csv_meta_file)
    dump_converter.write_entities_csv_row(identifier_pid, external_id, pid, value)

    # Run assertions
    expected_row = ",".join(str(v) for v in [dump_converter.data_source_item_id, identifier_pid, external_id, pid, value])
    assert expected_row == csv_entities_file.getvalue().rstrip("\r\n")

    # Close csv files
    csv_entities_file.close()
    csv_meta_file.close()


def test_write_meta_information():
    # Create file-like strings for csv output
    csv_entities_file = BytesIO()
    csv_meta_file = BytesIO()

    # Create dump converter and write csv
    dump_converter = create_dump_converter(csv_entities_file, csv_meta_file)
    dump_converter.data_source_urls = ["http://www.foo.bar"]
    dump_converter.write_meta_information()

    # Run assertions
    actual_row_fields = csv_meta_file.getvalue().rstrip("\r\n").split(",")
    assert str(dump_converter.data_source_item_id) == actual_row_fields[0]
    assert dump_converter.data_source_language == actual_row_fields[2]
    assert dump_converter.data_source_urls[0] == actual_row_fields[3]
    assert str(dump_converter.data_source_size) == actual_row_fields[4]
    assert dump_converter.data_source_license == actual_row_fields[5]

    # Close csv files
    csv_entities_file.close()
    csv_meta_file.close()


# Returns the size of a given file object
def get_file_size(file_obj):
    original_position = file_obj.tell()
    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(original_position)

    return size


# Creates dump converter instance for testing
def create_dump_converter(csv_entities_file=BytesIO(), csv_meta_file=BytesIO()):
    dump_converter = DumpConverter(
        csv_entities_file,
        csv_meta_file,
        True,
        42,
        42,
        "en",
        "CC0"
    )

    return dump_converter


if __name__ == "__main__":
    unittest.main()
import pytest
import unittest

import csv
import json

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
def test_print_progress(message, read_bytes, total_bytes, expected_output, capsys):
    DumpConverter.print_progress(message, read_bytes, total_bytes)

    out, err = capsys.readouterr()
    assert "\r\x1b[K" + expected_output == str(out)


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
    actual_row_fields = get_first_line_csv(csv_entities_file)
    assert str(dump_converter.data_source_item_id) == actual_row_fields[0]
    assert str(identifier_pid) == actual_row_fields[1]
    assert external_id == actual_row_fields[2]
    assert str(pid) == actual_row_fields[3]
    assert value == actual_row_fields[4]

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
    actual_row_fields = get_first_line_csv(csv_meta_file)
    assert str(dump_converter.data_source_item_id) == actual_row_fields[0]
    assert dump_converter.data_source_language == actual_row_fields[2]
    assert json.dumps(dump_converter.data_source_urls) == actual_row_fields[3]
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


# Returns the first line of a given csv file
def get_first_line_csv(csv_file):
    # Save position and go to beginning
    original_position = csv_file.tell()
    csv_file.seek(0)

    # Read first line
    csv_reader = csv.reader(csv_file)
    row = csv_reader.next()

    # Restore original position
    csv_file.seek(original_position)

    return row


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
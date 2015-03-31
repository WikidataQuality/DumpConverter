import pytest

import os
from io import BytesIO

import datetime

from dumpconverter.exceptions import DownloadError
from dumpconverter.GndDumpConverter import GndDumpConverter


@pytest.mark.parametrize("expected_value_quadruplets", [
    [
        (227, "119033364", 19, "Cambridge"),
        (227, "119033364", 20, "Santa Barbara, Calif."),
        (227, "119033364", 21, "m\xc3\xa4nnlich"),
        (227, '119033364', 50, 'Douglas Adams'),
        (227, '119033364', 569, '11.03.1952'),
        (227, '119033364', 570, '11.05.2001'),
        (227, '11876439X', 19, 'Wakefield'),
        (227, '11876439X', 20, 'Mount Vernon, Va.'),
        (227, '11876439X', 21, 'm\xc3\xa4nnlich'),
        (227, '11876439X', 26, 'Martha Washington'),
        (227, '11876439X', 50, 'George Washington'),
        (227, '11876439X', 569, '22.02.1732'),
        (227, '11876439X', 570, '14.12.1799')
    ]
])
def test_execute(expected_value_quadruplets):
    # Variable for counting number of external value quadruplets
    # In order to access this variable from inner function, array instead of integer is used (workaround)
    actual_value_count = [0]

    # Create mocked dump converter
    dump_converter = create_dump_converter()
    def download_dump_mock(dump_url):
        script_dir = os.path.dirname(__file__)
        return open(os.path.join(script_dir, "testdata/gnd_dump.xml.gz"), "rb")
    def write_entities_csv_row_mock(identifier_pid, external_id, pid, value):
        actual_value_count[0] += 1
        assert (identifier_pid, external_id, pid, value) in expected_value_quadruplets

    dump_converter.FILE_PREFIXES = ["foobar"]
    dump_converter.download_dump = download_dump_mock
    dump_converter.write_entities_csv_row = write_entities_csv_row_mock

    # Execute converter
    dump_converter.execute()

    # Run assertions
    assert len(expected_value_quadruplets) == actual_value_count[0]


def test_execute_error():
    with pytest.raises(DownloadError.DownloadError):
        # Create mocked dump converter
        dump_converter = create_dump_converter()
        def download_dump_mock(dump_url):
            raise DownloadError.DownloadError()
        dump_converter.download_dump = download_dump_mock

        # Execute converter
        dump_converter.execute()


@pytest.mark.parametrize(["prefix", "date", "fallback", "expected_url"], [
    # No fallback
    (
        "Tpgesamt",
        datetime.date(2015, 1, 1),
        False,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml143&mabheft=Tpgesamt1410gndmrc.xml.gz"
    ),
    (
        "Tpgesamt",
        datetime.date(2015, 2, 1),
        False,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml151&mabheft=Tpgesamt1502gndmrc.xml.gz"
    ),
    (
        "Tpgesamt",
        datetime.date(2015, 6, 1),
        False,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml152&mabheft=Tpgesamt1506gndmrc.xml.gz"
    ),
    (
        "Tpgesamt",
        datetime.date(2015, 10, 1),
        False,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml153&mabheft=Tpgesamt1510gndmrc.xml.gz"
    ),
    # Fallback
    (
        "Tpgesamt",
        datetime.date(2015, 1, 1),
        True,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml142&mabheft=Tpgesamt1406gndmrc.xml.gz"
    ),
    (
        "Tpgesamt",
        datetime.date(2015, 2, 1),
        True,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml143&mabheft=Tpgesamt1410gndmrc.xml.gz"
    ),
    (
        "Tpgesamt",
        datetime.date(2015, 6, 1),
        True,
        "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml151&mabheft=Tpgesamt1502gndmrc.xml.gz"
    )
])
def test_get_dump_url(prefix, date, fallback, expected_url):
    dump_converter = create_dump_converter()
    actual_url = dump_converter.get_dump_url(prefix, date=date, fallback=fallback)

    assert expected_url == actual_url


# Creates dump converter instance for testing
def create_dump_converter():
    dump_converter = GndDumpConverter(
        BytesIO(),
        BytesIO(),
        True
    )

    return dump_converter
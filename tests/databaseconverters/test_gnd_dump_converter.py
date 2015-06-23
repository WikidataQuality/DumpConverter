"""Contains test for GndDumpConverter class"""
import os
import datetime

import pytest
from mock import patch
from StringIO import StringIO

from dumpconverter.exceptions.DownloadError import DownloadError
from dumpconverter.writer.ResultWriter import ResultWriter
from dumpconverter.dataformatconverters.XmlDumpConverter import XmlDumpConverter
from dumpconverter.databaseconverters.gnd.GndDumpConverter import GndDumpConverter


@patch.object(ResultWriter, "write_dump_information")
@patch.object(ResultWriter, "write_external_value")
def test_execute(write_external_value_mock, write_dump_information_mock):
    script_dir = os.path.dirname(__file__)
    dump_file_path = os.path.join(script_dir, "testdata/gnd_dump.xml.gz")
    gnd_converter = GndDumpConverter(True)
    def download_dump_mock(file_prefix):
        dump_file = open(dump_file_path, "rb")
        return dump_file, None, None
    gnd_converter.download_dump = download_dump_mock
    gnd_converter.execute(ResultWriter(StringIO(), StringIO()))

    number_of_dumps = len(gnd_converter.FILE_PREFIXES)
    assert write_external_value_mock.call_count == 11 * number_of_dumps
    assert write_dump_information_mock.call_count == number_of_dumps


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
        datetime.date(2015, 4, 1),
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
    gnd_converter = GndDumpConverter()
    actual_url = gnd_converter.get_dump_url(prefix, date=date, fallback=fallback)

    assert expected_url == actual_url


@pytest.mark.parametrize(["dump_url", "fallback_url"], [
    ("200", "200"),
    ("400", "200"),
    ("500", "200"),
])
def test_download_dump_success(dump_url, fallback_url):
    @patch("dumpconverter.utils.downloadutils.download_file")
    def patched_wrapper(download_file_mock):
        expected_size = 42
        expected_prefix = "foobar"

        gnd_converter = GndDumpConverter()
        def get_dump_url_mock(file_prefix, fallback=False):
            assert expected_prefix == file_prefix
            if fallback:
                return fallback_url
            else:
                return dump_url
        gnd_converter.get_dump_url = get_dump_url_mock
        def download_file_mock_func(url, destination_file,
                               is_quiet=False, progress_message=""):
            if url == "200":
                return expected_size
            else:
                raise DownloadError(int(url))
        download_file_mock.side_effect = download_file_mock_func

        actual_file, actual_url, actual_size = gnd_converter.download_dump(expected_prefix)

        assert expected_size == actual_size

    patched_wrapper()


@patch("dumpconverter.utils.downloadutils.download_file",
       side_effect=DownloadError())
def test_download_dump_error(download_file_mock):
    with pytest.raises(DownloadError):
        gnd_converter = GndDumpConverter()
        gnd_converter.download_dump("foobar")


def test_write_external_data():
    expected_dump_id = "foobar"
    expected_value_triple = ("foobar", "P42", ["foobar"])

    gnd_converter = GndDumpConverter(False)
    xml_dump_converter_mock = XmlDumpConverter(None, None, None)
    def process_dump_mock(dump_file):
        yield expected_value_triple
    xml_dump_converter_mock.process_dump = process_dump_mock
    gnd_converter.xml_dump_converter = xml_dump_converter_mock
    result_mock = ResultWriter(StringIO(), StringIO())
    def write_external_value_mock(dump_id, external_id,
                                  property_id, external_value):
        assert expected_dump_id == dump_id
        assert expected_value_triple[0] == external_id
        assert expected_value_triple[1] == property_id
        assert external_value in expected_value_triple[2]
    result_mock.write_external_value = write_external_value_mock

    gnd_converter.write_external_data(expected_dump_id, None, result_mock)

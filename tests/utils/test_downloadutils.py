"""Contains test for downloadutils package"""
import pytest
from tempfile import TemporaryFile

from dumpconverter.exceptions import DownloadError
from dumpconverter.utils import downloadutils


@pytest.mark.parametrize(["url", "expected_content"], [
    (
        "http://httpstat.us/200",
        "200 OK"
    )
])
def test_download_file(url, expected_content):
    with TemporaryFile() as downloaded_file:
        file_size = downloadutils.download_file(url, downloaded_file, is_quiet=True)

        assert 0 == downloaded_file.tell()
        assert file_size > 0
        assert expected_content == downloaded_file.read()


@pytest.mark.parametrize("url", [
    "http://httpstat.us/204",
    "http://httpstat.us/404",
    "http://httpstat.us/418"
])
def test_download_dump_error(url):
    with pytest.raises(DownloadError.DownloadError):
        downloaded_file = TemporaryFile()
        downloadutils.download_file(url, downloaded_file, is_quiet=True)
"""Contains helper methods for downloading files."""
import urllib2

from dumpconverter.exceptions import DownloadError
import consoleutils

DOWNLOAD_TIMEOUT = 10
DOWNLOAD_BUFFER_SIZE = 8192


def download_file(url, destination_file,
                  is_quiet=False, progress_message="Downloading...{0}"):
    """
    Downloads file specified by url to given file object.
    :param url: Url of the file that should be downloaded
    :param destination_file: File, in which downloaded file should be written.
    :param is_quiet: If set to True, console output will be suppressed.
    :param progress_message: Message that shown on progress updates.
    :return: Size of downloaded file.
    """
    try:
        response = urllib2.urlopen(url, timeout=DOWNLOAD_TIMEOUT)
    except urllib2.URLError as exception:
        raise DownloadError.DownloadError(message=exception.reason)

    status_code = response.getcode()
    if status_code == 200:
        downloaded_bytes = 0
        total_bytes = get_content_length(response)

        while True:
            download_buffer = response.read(DOWNLOAD_BUFFER_SIZE)
            if not download_buffer:
                break

            downloaded_bytes += len(download_buffer)
            destination_file.write(download_buffer)

            if not is_quiet:
                consoleutils.print_progress(progress_message,
                                            downloaded_bytes, total_bytes)

        destination_file.flush()
        destination_file.seek(0)

        # Write new line to console to overwrite progress
        if not is_quiet:
            print

        return downloaded_bytes
    else:
        message = "HTTP response returned status code " + str(status_code)
        raise DownloadError.DownloadError(status_code, message)


def get_content_length(response):
    """
    Extracts the content length of a given response object.
    :param response: Response object.
    :return: Content length
    """
    meta = response.info()
    content_length = meta.getheaders("Content-Length")
    if len(content_length) > 0:
        return int(content_length[0])

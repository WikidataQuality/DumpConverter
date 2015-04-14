"""Contains abstract dump converter base class."""
import sys
import csv
import math
import json
import urllib2
import tempfile
import datetime

from exceptions import DownloadError


class DumpConverter(object):
    """
    Abstract dump converter, that is responsible for downloading dump files,
    running formatter and writing csv files.
    """
    DOWNLOAD_TIMEOUT = 10
    DOWNLOAD_BUFFER_SIZE = 8192

    def __init__(self, csv_entities_file, csv_meta_file,
                 is_quiet, source_item_id,  source_property_id,
                 data_source_language, data_source_license):
        """
        Creates new DumpConverter instance.
        :param csv_entities_file: File object for external entities.
        :param csv_meta_file: File object for meta information about the dump.
        :param is_quiet: If set to True, console output will be suppressed.
        :param source_item_id: Id of item of the data source.
        :param source_property_id: Id of property of the identifier of the data source.
        :param data_source_language: Code of the language of the data source.
        :param data_source_license: Id of item of the license of the data source.
        """
        self.is_quiet = is_quiet
        self.data_source_item_id = source_item_id
        self.data_source_property_id = source_property_id
        self.data_source_language = data_source_language
        self.data_source_license = data_source_license
        self.data_source_size = 0
        self.data_source_urls = []

        self.csv_entities_writer = csv.writer(csv_entities_file)
        self.csv_meta_writer = csv.writer(csv_meta_file)

    def download_dump(self, url):
        """
        Downloads dump specified by url to temporary file and returns it.
        :param url: Url of the dump that should be downloaded
        :return: File object of the downloaded dump.
        """
        try:
            response = urllib2.urlopen(url, timeout=self.DOWNLOAD_TIMEOUT)
        except urllib2.URLError as exception:
            raise DownloadError.DownloadError(exception.reason)

        status_code = response.getcode()
        if status_code == 200:
            meta = response.info()
            content_length = meta.getheaders("Content-Length")
            if len(content_length) > 0:
                total_bytes = int(content_length[0])
            else:
                total_bytes = -1

            downloaded_bytes = 0
            destination_file = tempfile.TemporaryFile()
            while True:
                download_buffer = response.read(self.DOWNLOAD_BUFFER_SIZE)
                if not download_buffer:
                    break

                downloaded_bytes += len(download_buffer)
                destination_file.write(download_buffer)

                if not self.is_quiet:
                    self.print_progress("Downloading database dump...{0}",
                                        downloaded_bytes, total_bytes)

            destination_file.flush()
            destination_file.seek(0)

            self.data_source_size += downloaded_bytes

            # Write new line to console to overwrite progress
            if not self.is_quiet:
                print

            return destination_file
        else:
            message = "HTTP response returned status code " + str(status_code)
            raise DownloadError.DownloadError(message)

    @staticmethod
    def print_progress(message, current_bytes, total_bytes=-1):
        """
        Prints progress of an i/o process.
        :param message: Message that should be shown in front of the progress.
        :param current_bytes: Number of current bytes.
        :param total_bytes: Number of total bytes.
        """
        if total_bytes > 0:
            progress = float(current_bytes) / total_bytes * 100
            message = message.format(str(round(progress, 2)) + "%")
        else:
            message = message.format(DumpConverter.format_bytes(current_bytes))

        sys.stdout.write("\r\033[K")
        sys.stdout.write(message),

    @staticmethod
    def format_bytes(bytes_count, precision=2):
        """
        Formats number of bytes to string with suitable unit.
        :param bytes_count: Number of bytes.
        :param precision: Precision of size number.
        :return: Formatted string with suitable unit.
        """
        if bytes_count > 0:
            units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            exponent = int(math.floor(math.log(bytes_count, 1024)))
            power = math.pow(1024, exponent)
            converted = round(bytes_count / power, precision)
            if converted > 0:
                return '%s %s' % (converted, units[exponent])

        return '0 B'

    @staticmethod
    def run_formatter(formatter, nodes):
        """
        Runs given formatter on specified list of nodes.
        Any exceptions raised in formatter will be ignored
        :param formatter: String that contains formatter as python code.
        :param nodes: List of nodes, on which the formatter should work.
        :return: Result of the formatter. If exception was raised, None.
        """
        try:
            return eval(formatter)
        except:
            pass

    def write_entities_csv_row(self, identifier_pid, external_id, pid, value):
        """
        Write single row to entities csv file.
        :param identifier_pid: Id of property of the identifier of the data source.
        :param external_id: Id of the entity from dump.
        :param pid: Id of the property.
        :param value: Id of the value for the property.
        """
        row = (
            self.data_source_item_id,
            identifier_pid,
            external_id,
            pid,
            value
        )
        self.csv_entities_writer.writerow(row)

    def write_meta_information(self):
        """
        Writes data source meta information to csv file
        """
        row = (
            self.data_source_item_id,
            datetime.datetime.utcnow(),
            self.data_source_language,
            json.dumps(self.data_source_urls),
            self.data_source_size,
            self.data_source_license
        )
        self.csv_meta_writer.writerow(row)

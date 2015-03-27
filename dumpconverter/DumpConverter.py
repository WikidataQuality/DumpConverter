import csv
import sys
import math
import urllib2
import tempfile
import datetime

from exceptions import DownloadError


class DumpConverter(object):
    # Download parameter
    DOWNLOAD_TIMEOUT = 10
    DOWNLOAD_BUFFER_SIZE = 8192

    def __init__(self, csv_entities_file, csv_meta_file, is_quiet, source_item_id, source_property_id, data_source_language, data_source_license):
        self.is_quiet = is_quiet
        self.data_source_item_id = source_item_id
        self.data_source_property_id = source_property_id
        self.data_source_language = data_source_language
        self.data_source_license = data_source_license
        self.data_source_size = 0
        self.data_source_urls = []

        # Initialize csv writer
        self.csv_entities_writer = csv.writer(csv_entities_file)
        self.csv_meta_writer = csv.writer(csv_meta_file)

    # Downloads dump specified by url to temporary file and returns it.
    def download_dump(self, url):
        # Initialize download
        try:
            response = urllib2.urlopen(url, timeout=self.DOWNLOAD_TIMEOUT)
        except urllib2.URLError as e:
            raise DownloadError.DownloadError(e.reason.strerror)

        # Check, if request was successful
        http_status_code = response.getcode()
        if http_status_code == 200:
            # Get total size
            meta = response.info()
            content_length = meta.getheaders("Content-Length")
            if len(content_length) > 0:
                total_bytes = int(content_length[0])
            else:
                total_bytes = -1

            # Start download
            downloaded_bytes = 0
            destination_file = tempfile.TemporaryFile()
            while True:
                # Read block
                download_buffer = response.read(self.DOWNLOAD_BUFFER_SIZE)
                if not download_buffer:
                    break

                # Write block to file
                downloaded_bytes += len(download_buffer)
                destination_file.write(download_buffer)

                # Show progress
                if not self.is_quiet:
                    self.print_progress("Downloading database dump...{0}", downloaded_bytes, total_bytes)

            # Flush file at end and move read/write pointer to beginning of file
            destination_file.flush()
            destination_file.seek(0)

            # Set file size
            self.data_source_size += downloaded_bytes

            # Write new line to console to now overwrite progress
            sys.stdout.write("\n")

            return destination_file
        else:
            raise DownloadError.DownloadError("HTTP response returned status code" + http_status_code)

    # Prints progress of an i/o process.
    @staticmethod
    def print_progress(message, read_bytes, total_bytes=-1):
        if total_bytes > 0:
            # Calculate and print progress
            progress = float(read_bytes) / total_bytes * 100
            message = message.format(round(progress, 2) + "%")
        else:
            # Print only processed size as total size is unknown
            message = message.format(DumpConverter.format_bytes(read_bytes))

        message += "\r"
        sys.stdout.write(message )

    # Formats number of bytes to string with suitable unit.
    @staticmethod
    def format_bytes(bytes, precision=2):
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(bytes, 1024)))
        p = math.pow(1024, i)
        s = round(bytes / p, precision)
        if s > 0:
            return '%s %s' % (s, units[i])
        else:
            return '0 B'

    # Runs given formatter on specified list of nodes.
    @staticmethod
    def run_formatter(formatter, nodes):
        try:
            return eval(formatter)
        except:
            pass

    # Write single row to entities csv file
    def write_entities_csv_row(self, identifier_pid, external_id, pid, value):
        row = (
            self.data_source_item_id,
            identifier_pid,
            external_id,
            pid,
            value
        )
        self.csv_entities_writer.writerow(row)

    # Writes data source meta information to csv file
    def write_meta_information(self):
        row = (
            self.data_source_item_id,
            datetime.datetime.utcnow(),
            self.data_source_language,
            ", ".join(self.data_source_urls),
            self.data_source_size,
            self.data_source_license
        )
        self.csv_meta_writer.writerow(row)
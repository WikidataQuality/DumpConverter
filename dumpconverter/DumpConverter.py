import csv
import sys
import math
import urllib2
import tempfile


class DumpConverter(object):
    # Download parameter
    DOWNLOAD_TIMEOUT = 10
    DOWNLOAD_BUFFER_SIZE = 8192

    def __init__(self, csv_entities_file, csv_meta_file, source_item_id, source_property_id, data_source_language, data_source_license):
        self.data_source_item_id = source_item_id
        self.data_source_property_id = source_property_id
        self.data_source_language = data_source_language
        self.data_source_url = self.get_data_source_url()
        self.data_source_license = data_source_license
        self.data_source_size = 0

        # Initialize csv writer
        self.csv_entities_writer = csv.writer(csv_entities_file)
        self.csv_meta_writer = csv.writer(csv_meta_file)

    # Downloads latest dump to temporary file and returns it.
    def download_dump(self):
        # Initialize download
        response = urllib2.urlopen(self.data_source_url, timeout=self.DOWNLOAD_TIMEOUT)

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
            buffer = response.read(self.DOWNLOAD_BUFFER_SIZE)
            if not buffer:
                break

            # Write block to file
            downloaded_bytes += len(buffer)
            destination_file.write(buffer)

            # Show progress
            self.print_download_progress(downloaded_bytes, total_bytes)

        # Flush file at end and move read/write pointer to beginning of file
        destination_file.flush()
        destination_file.seek(0)

        # Set file size
        self.data_source_size = downloaded_bytes

        # Write new line to console to now overwrite progress
        sys.stdout.write("\n")

        return destination_file

    # Prints progress of download to console.
    @staticmethod
    def print_download_progress(downloaded_bytes, total_bytes):
        sys.stdout.write("Downloading database dump... ")
        if total_bytes > 0:
            # Calculate and print progress
            progress = float(downloaded_bytes) / total_bytes * 100
            sys.stdout.write("{0}%\r".format(round(progress, 2)))
        else:
            # Print only downloaded size as total size is unknown
            sys.stdout.write("{0}\r".format(DumpConverter.format_bytes(downloaded_bytes)))

    # Prints progress of processing dump to console.
    @staticmethod
    def print_processing_progress(processed_bytes, total_bytes=-1):
        sys.stdout.write("Processing database dump... ")
        if total_bytes > 0:
            # Calculate and print progress
            progress = float(processed_bytes) / total_bytes * 100
            sys.stdout.write("{0}%\r".format(round(progress, 2)))
        else:
            # Print only processed size as total size is unknown
            sys.stdout.write("{0}\r".format(DumpConverter.format_bytes(processed_bytes)))

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

    # Write single row to entities csv file
    def write_entities_csv_row(self, identifier_pid, external_id, pid, value):
        row = (identifier_pid, external_id, pid, value.encode("utf-8"))
        self.csv_entities_writer.writerow(row)

    # Writes data source meta information to csv file
    def write_meta_information(self):
        row = (
            self.data_source_item_id,
            self.data_source_language,
            self.data_source_url,
            self.data_source_size,
            self.data_source_license
        )
        self.csv_meta_writer.writerow(row)
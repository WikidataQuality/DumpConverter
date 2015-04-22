"""Contains dump converter for dumps of the Integrated Authority File."""
import datetime
from gzip import GzipFile
from tempfile import TemporaryFile

from XmlDumpConverter import XmlDumpConverter
from dumpconverter.propertymappings import gnd
from dumpconverter.utils import downloadutils
from dumpconverter.exceptions.DownloadError import DownloadError
from dumpconverter.writer.ResultWriter import ResultWriter


class GndDumpConverter():
    """
    Dump converter for dumps of the Integrated Authority File (GND) of the
    German National Library. Downloads latest dump files, processes entities and
    writes values to tar file.
    """
    DATA_SOURCE_ITEM_ID = "Q36578"
    IDENTIFIER_PROPERTY_ID = "P227"
    LANGUAGE = "de"
    LICENSE_ITEM_ID = "Q6938433"

    FILE_PREFIXES = {
        "GND-Tpgesamt": "Tpgesamt",
        "GND-Tggesamt": "Tggesamt",
        "GND-Tugesamt": "Tugesamt"
    }
    URL_FORMAT = "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml{0}{1}&mabheft={2}{0}{3}gndmrc.xml.gz"

    XML_ENTITIES_PATH = "ns:collection/ns:record"
    XML_ENTITY_ID_XPATH = "substring-after(ns:datafield[@tag='035']/ns:subfield[@code='a' and starts-with(./text(), '(DE-588)')], '(DE-588)')"
    XML_NAMESPACES = {
        "ns": "http://www.loc.gov/MARC21/slim"
    }

    def __init__(self, is_quiet=False):
        """
        Creates new GndDumpConverter instance.
        :param is_quiet: If set to True, console output will be suppressed.
        """
        self.is_quiet = is_quiet
        self.xml_dump_converter = XmlDumpConverter(self.XML_ENTITIES_PATH,
                                                   self.XML_ENTITY_ID_XPATH,
                                                   gnd.property_mapping,
                                                   self.XML_NAMESPACES,
                                                   is_quiet)

    def execute(self, output_file_path):
        """
        Starts whole convert process.
        :param output_file_path: File object for results.
        """
        result = ResultWriter()

        for dump_id, file_prefix in self.FILE_PREFIXES.iteritems():
            if not self.is_quiet:
                print "Start to convert '{0}'".format(file_prefix)

            dump_file, dump_url, dump_size = self.download_dump(file_prefix)

            uncompressed_dump_file = GzipFile(mode="rb", fileobj=dump_file)

            self.write_external_data(dump_id, uncompressed_dump_file, result)
            result.write_identifier_property(
                self.IDENTIFIER_PROPERTY_ID,
                dump_id)
            result.write_dump_information(
                dump_id,
                self.DATA_SOURCE_ITEM_ID,
                self.LANGUAGE,
                dump_url,
                dump_size,
                self.LICENSE_ITEM_ID)

            uncompressed_dump_file.close()
            dump_file.close()

            if not self.is_quiet:
                print

        result.to_archive(output_file_path)
        result.close()

    def get_dump_url(self, file_prefix, fallback=False, date=datetime.date.today()):
        """
        Returns url of the latest dump with specified prefix.
        If dump file does not exist, fallback option can be set True to
        build url of previous dump.
        This will be applicable, if new dump should be already available,
        but was not published yet.
        :param file_prefix: Prefix of the dump file.
        :param fallback: If set to True, url of previous dump will be returned.
        :param date: Datetime, on which the url generation is based on.
        :return: Url of the dump
        """
        if fallback:
            previous_month = date.month - 4
            previous_year = date.year
            if previous_month <= 0:
                previous_month = (date.month - 4) % 12
                if previous_month == 0:
                    previous_month = 12
                previous_year -= 1
            date = datetime.date(previous_year, previous_month, 1)

        year = date.year
        if date.month == 1:
            index = 3
            month = "10"
            year -= 1
        elif date.month < 6:
            index = 1
            month = "02"
        elif date.month < 10:
            index = 2
            month = "06"
        else:
            index = 3
            month = "10"
        year = str(year)[-2:]

        return self.URL_FORMAT.format(year, index, file_prefix, month)

    def download_dump(self, file_prefix):
        """
        Downloads a dump identified by file prefix to destination file.
        :param file_prefix: Prefix of the dump file.
        :param destination_file: Destination file object.
        :return: List of url and size of downloaded file.
        """
        dump_file = TemporaryFile()
        dump_url = self.get_dump_url(file_prefix)
        try:
            dump_size = downloadutils.download_file(dump_url, dump_file,
                                                    is_quiet=self.is_quiet,
                                                    progress_message="Downloading database dump...{0}")
        except DownloadError as e:
            if e.status_code == 400 or e.status_code == 500:
                dump_url = self.get_dump_url(file_prefix, fallback=True)
                dump_size = downloadutils.download_file(dump_url, dump_file,
                                                        is_quiet=self.is_quiet,
                                                        progress_message="Downloading database dump...{0}")
            else:
                raise

        return dump_file, dump_url, dump_size

    def write_external_data(self, dump_id, dump_file, result):
        """
        Processes dump and writes external values to file.
        :param dump_id: Id of the processing dump.
        :param dump_file: File object of the dump.
        :param result: Current result writer.
        """
        external_data = self.xml_dump_converter.process_dump(dump_file)
        for external_id, property_id, external_values in external_data:
            for external_value in external_values:
                result.write_external_value(dump_id, external_id,
                                            property_id, external_value)

"""Contains dump converter for dumps of the Integrated Authority File."""
import gzip
import datetime

from XmlDumpConverter import *
from exceptions import DownloadError
from propertymappings import gnd


class GndDumpConverter(XmlDumpConverter):
    """
    Dump converter for dumps of the Integrated Authority File (GND) of the
    German National Library. Downloads latest dump files, processes entities and
    writes values to csv files.
    """
    ITEM_ID = 36578
    PROPERTY_ID = 227
    LANGUAGE = "de"
    LICENSE = "CC0 1.0"

    FILE_PREFIXES = [
        "Tpgesamt",
        "Tggesamt",
        "Tugesamt"
    ]
    URL_FORMAT = "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml{0}{1}&mabheft={2}{0}{3}gndmrc.xml.gz"

    XML_NAMESPACE_MAP = {
        "ns": "http://www.loc.gov/MARC21/slim"
    }
    XML_ENTITIES_XPATH = "ns:collection/ns:record"
    XML_ENTITY_ID_XPATH = "ns:controlfield[@tag='001']/text()"

    def __init__(self, csv_entities_file, csv_meta_file, is_quiet):
        """
        Creates new GndDumpConverter instance.
        :param csv_entities_file: File object for external entities.
        :param csv_meta_file: File object for meta information about the dump.
        :param is_quiet: If set to True, console output will be suppressed.
        """
        super(GndDumpConverter, self).__init__(
            csv_entities_file,
            csv_meta_file,
            is_quiet,
            self.ITEM_ID,
            self.PROPERTY_ID,
            self.LANGUAGE,
            self.LICENSE,
            self.XML_NAMESPACE_MAP,
            self.XML_ENTITIES_XPATH,
            self.XML_ENTITY_ID_XPATH,
            gnd.property_mapping)

        self.dump_urls = []

    def execute(self):
        """
        Starts whole convert process.
        """
        for file_prefix in self.FILE_PREFIXES:
            if not self.is_quiet:
                print "Start to convert '{0}'".format(file_prefix)

            dump_url = self.get_dump_url(file_prefix)

            try:
                dump_file = self.download_dump(dump_url)
            except DownloadError.DownloadError:
                dump_url = self.get_dump_url(file_prefix, fallback=True)
                dump_file = self.download_dump(dump_url)

            uncompressed_dump_file = gzip.GzipFile(mode="rb", fileobj=dump_file)

            process_dump_generator = self.process_dump(uncompressed_dump_file)
            if process_dump_generator:
                for external_id, property_id, external_values in process_dump_generator:
                    for external_value in external_values:
                        self.write_entities_csv_row(self.PROPERTY_ID, external_id,
                                                    property_id, external_value)

            uncompressed_dump_file.close()
            dump_file.close()

            self.data_source_urls.append(dump_url)

            if not self.is_quiet:
                print

        self.write_meta_information()

    def get_dump_url(self, prefix, fallback=False, date=datetime.date.today()):
        """
        Returns url of the latest dump with specified prefix.
        If dump file does not exist, fallback option can be set True to
        build url of previous dump.
        This will be applicable, if new dump should be already available,
        but was not published yet.
        :param prefix: Prefix of the dump file.
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

        return self.URL_FORMAT.format(year, index, prefix, month)

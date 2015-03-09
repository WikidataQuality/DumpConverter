import gzip
import datetime

from XmlDumpConverter import *
from propertymappings import gnd


class GndDumpConverter(XmlDumpConverter):
    # Data source properties
    DATA_SOURCE_LANGUAGE = "de"
    DATA_SOURCE_LICENSE = "CC0 1.0"
    DATA_SOURCE_ITEM_ID = "36578"
    DATA_SOURCE_PROPERTY_ID = "227"
    DATA_SOURCE_URL_FORMAT = "http://datendienst.dnb.de/cgi-bin/mabit.pl?cmd=fetch&userID=GNDxml&pass=gndmarcxml{0}{1}&mabheft=Tpgesamt{0}{2}gndmrc.xml.gz"
    XML_NAMESPACE_MAP = {
        "ns": "http://www.loc.gov/MARC21/slim"
    }
    XML_ENTITIES_PATH = "ns:collection/ns:record"
    XML_ENTITY_ID_PATH = "ns:controlfield[@tag='001']/text()"

    def __init__(self, csv_entities_file, csv_meta_file):
        super(GndDumpConverter, self).__init__(
            csv_entities_file,
            csv_meta_file,
            self.DATA_SOURCE_ITEM_ID,
            self.DATA_SOURCE_PROPERTY_ID,
            self.DATA_SOURCE_LANGUAGE,
            self.DATA_SOURCE_LICENSE,
            self.XML_NAMESPACE_MAP,
            self.XML_ENTITIES_PATH,
            self.XML_ENTITY_ID_PATH,
            gnd.property_mapping)

    # Starts whole convert process.
    def execute(self):
        # Download dump
        dump_file = self.download_dump()

        # Open compressed dump as gzip file
        uncompressed_dump_file = gzip.GzipFile(mode="rb", fileobj=dump_file)

        # Process dump
        for external_id, property_id, external_values in self.process_dump(uncompressed_dump_file):
            for external_value in external_values:
                self.write__entities_csv_row(self.DATA_SOURCE_PROPERTY_ID, external_id, property_id, external_value)

        # Close file
        uncompressed_dump_file.close()
        dump_file.close()

        # Write meta information
        self.write_meta_information()

    # Returns url of the latest dump.
    # If fallback option is set to True, url of previous dump will be returned.
    def get_data_source_url(self, fallback=False):
        now = datetime.date.today()

        # If dump file does not exist, fallback option can be set True to build url of previous dump.
        # This will be applicable, if new dump should be already available, but was not published yet.
        if fallback:
            previous_month = now.month - 4
            if previous_month <= 0:
                previous_month = (now.month - 4) % 12
            now = datetime.date(now.year - 1, previous_month, now.day)

        # Set parameter depending on month
        if now.month == 1:
            index = 3
            month = "10"
            now.year -= 1
        elif now.month < 6:
            index = 1
            month = "02"
        elif now.month < 10:
            index = 2
            month = "06"
        else:
            index = 3
            month = "10"
        year = now.strftime("%y")

        return self.DATA_SOURCE_URL_FORMAT.format(year, index, month)
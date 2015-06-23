"""Contains class for writing conversion results to file."""
import csv
from datetime import datetime
import json


class ResultWriter:
    """
    Contains writer for writing conversion result to csv files.
    """

    def __init__(self, external_values_file, dump_information_file):
        """
        Creates new ResultWriter instance.
        :param external_values_file: File for output of external values.
        :param dump_information_file: File for output of metadata of the dump.
        """
        self.external_data_writer = csv.writer(external_values_file)
        self.dump_information_writer = csv.writer(dump_information_file)

    def write_external_value(self, dump_id, external_id,
                             property_id, value):
        """
        Writes single external value to file.
        :param dump_id: Id of the current dump.
        :param external_id: Id of the external entity.
        :param property_id: Id of the Wikidata property.
        :param value: Data value of external entity for the Wikidata property.
        """
        row = (
            dump_id,
            external_id,
            property_id,
            value
        )
        self.external_data_writer.writerow(row)

    def write_dump_information(self, dump_id, data_source_item_id,
                               identifier_property_ids, language,
                               source_url, size, license_item_id):
        """
        Writes meta information about a single dump to file.
        :param dump_id: Id of the dump.
        :param data_source_item_id: Id of the Wikidata item of the data source.
        :param identifier_property_ids: Ids of Wikidata properties for identifiers of the data source.
        :param language: Language code.
        :param source_url: Source url.
        :param size: File size in bytes.
        :param license_item_id: Id of the Wikidata item of the license.
        :return:
        """
        row = (
            dump_id,
            data_source_item_id,
            json.dumps(identifier_property_ids),
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            language,
            source_url,
            size,
            license_item_id
        )
        self.dump_information_writer.writerow(row)

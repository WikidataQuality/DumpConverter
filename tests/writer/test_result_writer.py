"""Contains tests for ResultWriter class"""
import csv
import json
import unittest
from StringIO import StringIO

from dumpconverter.writer.ResultWriter import ResultWriter


class ResultWriterTest(unittest.TestCase):
    def test_write_external_data(self):
        dump_id = "foobar"
        external_id = "foobar"
        property_id = "P42"
        value = "foobar"

        dump_information_file = StringIO()
        external_data_file = StringIO()
        result = ResultWriter(external_data_file, dump_information_file)
        result.write_external_value(dump_id, external_id, property_id, value)

        actual_row_fields = self.get_first_line_csv(external_data_file)

        assert dump_id == actual_row_fields[0]
        assert external_id == actual_row_fields[1]
        assert property_id == actual_row_fields[2]
        assert value == actual_row_fields[3]

    def test_write_dump_information(self):
        dump_id = "foobar"
        data_source_item_id = "Q42"
        identifier_property_ids = ["P42"]
        language = "en"
        source_url = "http://foo.bar"
        size = 42
        license_item_id = "Q21"

        dump_information_file = StringIO()
        external_data_file = StringIO()
        result = ResultWriter(external_data_file, dump_information_file)
        result.write_dump_information(dump_id, data_source_item_id,
                                      identifier_property_ids, language,
                                      source_url, size, license_item_id)

        actual_row_fields = self.get_first_line_csv(dump_information_file)

        assert dump_id == actual_row_fields[0]
        assert data_source_item_id == actual_row_fields[1]
        assert identifier_property_ids == json.loads(actual_row_fields[2])
        assert language == actual_row_fields[4]
        assert source_url == actual_row_fields[5]
        assert str(size) == actual_row_fields[6]
        assert license_item_id == actual_row_fields[7]

    # Returns the first line of a given csv file
    def get_first_line_csv(self, csv_file):
        original_position = csv_file.tell()
        csv_file.seek(0)

        csv_reader = csv.reader(csv_file)
        row = csv_reader.next()

        csv_file.seek(original_position)

        return row


if __name__ == "__main__":
    unittest.main()

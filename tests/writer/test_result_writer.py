"""Contains tests for ResultWriter class"""
import os
import csv
import tarfile
import unittest
from tempfile import TemporaryFile

from dumpconverter.writer.ResultWriter import ResultWriter


class ResultWriterTest(unittest.TestCase):
    def setUp(self):
        self.test_archive_name = "test_archive.tar"

    def tearDown(self):
        if os.path.isfile(self.test_archive_name):
            os.remove(self.test_archive_name)

    def test_write_external_data(self):
        dump_id = "foobar"
        external_id = "foobar"
        property_id = "P42"
        value = "foobar"

        result = ResultWriter()
        result.write_external_value(dump_id, external_id, property_id, value)

        actual_row_fields = self.get_first_line_csv(result.external_data_file)
        result.close()

        assert dump_id == actual_row_fields[0]
        assert external_id == actual_row_fields[1]
        assert property_id == actual_row_fields[2]
        assert value == actual_row_fields[3]

    def test_write_dump_information(self):
        data_source_item_id = "Q42"
        language = "en"
        source_url = "http://foo.bar"
        size = 42
        license_item_id = "Q21"

        result = ResultWriter()
        result.write_dump_information(data_source_item_id, language,
                                      source_url, size, license_item_id)

        actual_row_fields = self.get_first_line_csv(result.dump_information_file)
        result.close()

        assert data_source_item_id == actual_row_fields[0]
        assert language == actual_row_fields[2]
        assert source_url == actual_row_fields[3]
        assert str(size) == actual_row_fields[4]
        assert license_item_id == actual_row_fields[5]

    def test_write_identifier_property(self):
        identifier_property_id = "P42"
        dump_id = "foobar"

        result = ResultWriter()
        result.write_identifier_property(identifier_property_id, dump_id)

        actual_row_fields = self.get_first_line_csv(result.identifier_properties_file)
        result.close()

        assert identifier_property_id == actual_row_fields[0]
        assert dump_id == actual_row_fields[1]

    def test_to_archive(self):
        result = ResultWriter()
        result.to_archive(self.test_archive_name)

        with tarfile.open(self.test_archive_name) as tar_file:
            actual_names = self.get_file_names(tar_file)
            expected_names = [ResultWriter.EXTERNAL_DATA_FILE_NAME,
                              ResultWriter.DUMP_INFORMATION_FILE_NAME,
                              ResultWriter.IDENTIFIER_PROPERTIES_FILE_NAME]
            assert sorted(actual_names) == sorted(expected_names)

    def test_add_file_to_tar(self):
        expected_file_name = "foobar"
        with TemporaryFile() as file_to_add:
            with tarfile.open(self.test_archive_name, mode="w:gz") as tar_file:
                ResultWriter.add_file_to_tar(tar_file,
                                             expected_file_name, file_to_add)
                assert [expected_file_name] == self.get_file_names(tar_file)

    def test_close(self):
        result = ResultWriter()
        result.close()

        assert result.external_data_file.closed
        assert result.dump_information_file.closed
        assert result.identifier_properties_file.closed

    # Returns the first line of a given csv file
    def get_first_line_csv(self, csv_file):
        original_position = csv_file.tell()
        csv_file.seek(0)

        csv_reader = csv.reader(csv_file)
        row = csv_reader.next()

        csv_file.seek(original_position)

        return row

    def get_file_names(self, tar_file):
        return map(lambda tar_info: tar_info.name, tar_file.getmembers())


if __name__ == "__main__":
    unittest.main()

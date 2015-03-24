import unittest

from testtools import TestCase
from testtools.matchers import Equals

from unittest_data_provider import data_provider

from dumpconverter.DumpConverter import DumpConverter


class DumpConverterTest(TestCase):
    def setUp(self):
        # Open csv files
        TestCase.setUp(self)
        self.csv_entities_file = open("entities.csv", "wb")
        self.csv_meta_file = open("meta.csv", "wb")
        self.testdata = (
            (
                "nodes[0].split('-')[0]",
                ["01.01.2015-31.12.2015"],
                "01.01.2015"
            ),
            (
                "nodes[1] + ' ' + nodes[0]",
                ["Adams", "Douglas"],
                "Douglas Adams"
            ),
            (
                "nodes[0] + nodes[1]",
                ["foo", "bar"],
                "foobar"
            ),
            (
                "nodes[1]",
                ["foobar"],
                None
            )
        )

    def tearDown(self):
        # Close csv files
        self.csv_entities_file.close()
        self.csv_meta_file.close()
        TestCase.tearDown(self)

    def test_run_formatter(self):
        dump_converter = self.create_dump_converter()
        for data in self.testdata:
            formatter = data[0]
            nodes = data[1]
            expected_result = data[2]
            actual_result = dump_converter.run_formatter(formatter, nodes)
            self.assertThat(actual_result, Equals(expected_result))

    def create_dump_converter(self):
        dump_converter = DumpConverter(
            self.csv_entities_file,
            self.csv_meta_file,
            0,
            42,
            42,
            "en",
            "CC0"
        )

        return dump_converter


if __name__ == "__main__":
    unittest.main()
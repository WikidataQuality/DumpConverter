import unittest

from testtools import TestCase
from testtools.matchers import Equals

from unittest_data_provider import data_provider

from dumpconverter.DumpConverter import DumpConverter


class DumpConverterTest(TestCase):
    def setUp(self):
        # Open csv files
        self.csv_entities_file = open("entities.csv", "wb")
        self.csv_meta_file = open("meta.csv", "wb")

    def tearDown(self):
        # Close csv files
        self.csv_entities_file.close()
        self.csv_meta_file.close()

    run_formatter_data_provider = (
        (
            "nodes[0].split('-')[0]",
            ["01.01.2015-31.12.2015"],
            "01.01.2015"
        ),
        (
            "nodes[1] + ',' + nodes[0]",
            ["Adams, Douglas"],
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

    @data_provider(run_formatter_data_provider)
    def test_run_formatter(self, formatter, nodes, expected_result):
        dump_converter = self.create_dump_converter()
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
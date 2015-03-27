import unittest

from testtools import TestCase
from testtools.matchers import Equals

from ddt import ddt, data, unpack

from io import StringIO

from dumpconverter.DumpConverter import DumpConverter


@ddt
class DumpConverterTest(TestCase):
	def setUp(self):
		super(DumpConverterTest, self).setUp()

		# Create file-like strings for csv output
		self.csv_entities_file = StringIO()
		self.csv_meta_file = StringIO()

	def tearDown(self):
		# Close csv strings
		self.csv_entities_file.close()
		self.csv_meta_file.close()

		super(DumpConverterTest, self).tearDown()

	@data(
		(
			"nodes[0].split('-')[0]",
			["01.01.2015-31.12.2015"],
			"01.01.2015"
		),
		(
			"nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]",
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
	@unpack
	def test_run_formatter(self, formatter, nodes, expected_result):
		dump_converter = self.create_dump_converter()
		actual_result = dump_converter.run_formatter(formatter, nodes)
		self.assertThat(actual_result, Equals(expected_result))

	def create_dump_converter(self):
		dump_converter = DumpConverter(
			self.csv_entities_file,
			self.csv_meta_file,
			True,
			42,
			42,
			"en",
			"CC0"
		)

		return dump_converter


if __name__ == "__main__":
	unittest.main()
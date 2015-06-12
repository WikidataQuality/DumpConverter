from writer.ResultWriter import ResultWriter
from dumpconverter.databaseconverters.gnd.GndDumpConverter import *

class DumpConverter:
    """
    Wrapper class, that executes multiple dump dataformatconverters.
    """
    # Available dump converter with their key and description
    DATABASES = {
        "gnd": {
            "converter": GndDumpConverter,
            "description": "Integrated Authority File of the German National Library."
        }
    }

    def __init__(self, output_file_path, database=None, is_quiet=False):
        """
        Creates new DumpConverter instance.
        :param database: Key of the database, that should be converted
                         or None to convert all available databases.
        :param output_file_path: Path of the output file.
        :param is_quiet: If set to True, console output will be suppressed.
        """
        self.output_file_path = output_file_path
        self.database = database
        self.is_quiet = is_quiet

    def execute(self):
        """
        Runs the specified converters.
        """
        result_writer = ResultWriter()

        if self.database:
            if self.database not in self.DATABASES:
                print "No converter with specified key found!"
                return False
            self.run_converter(self.database.lower(), result_writer)
        else:
            for converter_key in self.DATABASES.iterkeys():
                self.run_converter(converter_key, result_writer)

        result_writer.to_archive(self.output_file_path)
        result_writer.close()

        return True

    def run_converter(self, converter_key, result_writer):
        """
        Runs specific converter
        :param converter_key: Name of the converter.
        :param result_writer: Writer for output of results.
        """
        importer = self.DATABASES[converter_key]["converter"](self.is_quiet)
        importer.execute(result_writer)

    @staticmethod
    def get_available_databases():
        """
        Gets database available for conversions
        :return: Dictionary key of a database and its description
        """
        return map(
            lambda (key, value): (key, value["description"]),
            DumpConverter.DATABASES.items())

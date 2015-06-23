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

    def __init__(self, external_values_file, dump_information_file, database=None, is_quiet=False):
        """
        Creates new DumpConverter instance.
        :param database: Key of the database, that should be converted
                         or None to convert all available databases.
        :param external_values_file: File object for output of external values.
        :param dump_information_file: File object for output of metadata of the dump.
        :param is_quiet: If set to True, console output will be suppressed.
        """
        self.database = database
        self.is_quiet = is_quiet
        self.result_writer = ResultWriter(external_values_file, dump_information_file)

    def execute(self):
        """
        Runs the specified converters.
        """
        if self.database:
            if self.database not in self.DATABASES:
                print "No converter with specified key found!"
                return False
            self.run_converter(self.database.lower())
        else:
            for converter_key in self.DATABASES.iterkeys():
                self.run_converter(converter_key)

        return True

    def run_converter(self, converter_key):
        """
        Runs specific converter
        :param converter_key: Name of the converter.
        """
        importer = self.DATABASES[converter_key]["converter"](self.is_quiet)
        importer.execute(self.result_writer)

    @staticmethod
    def get_available_databases():
        """
        Gets database available for conversions
        :return: Dictionary key of a database and its description
        """
        return map(
            lambda (key, value): (key, value["description"]),
            DumpConverter.DATABASES.items())

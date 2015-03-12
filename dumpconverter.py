import argparse

from dumpconverter.GndDumpConverter import *


# Available dump converter with their key name
importers = {
    "gnd": GndDumpConverter
}


def run():
    # Parse arguments
    parser = argparse.ArgumentParser(description="This program downloads dumps from a specified data source and converts it to CSV data.")
    parser.add_argument("data_source", help="Name of the data source that should be imported.")
    parser.add_argument("entities_output", help="The CSV output file for external entities.")
    parser.add_argument("meta_output", help="The CSV output file for meta information about the data source.")
    args = parser.parse_args()

    # Open output files
    csv_entities_file = open(args.entities_output, "wb")
    csv_meta_file = open(args.meta_output, "wb")

    # Instantiate requested importer
    importer_name = args.data_source.lower()
    if importer_name in importers:
        importer = importers[importer_name](csv_entities_file, csv_meta_file)
    else:
        print "No importer with specified name found!"
        return

    # Run import
    importer.execute()

    # Close file handles
    csv_entities_file.close()
    csv_meta_file.close()


if __name__ == "__main__":
    run()
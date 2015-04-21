"""Main script that executes dump converters and writes results to csv files."""
import argparse

from tabulate import tabulate

from dumpconverter.converters.GndDumpConverter import *


# Available dump converter with their key name
importers = {
    "gnd": {
        "class": GndDumpConverter,
        "description": "Integrated Authority File of the German National Library."
    }
}


def run():
    parser = argparse.ArgumentParser(description="This program downloads dumps from one or many databases and converts them into a format, that can be imported by WikidataQualityExternalValidation extension.")
    parser.add_argument("--list-databases", help="list all available databases, that can be imported, and exit", action="store_true")
    parser.add_argument("--database", "-d", help="name of a specific database that should be imported.")
    parser.add_argument("--output-file", "-o", help="TAR output file for data values of dumps.", default="external_data.tar")
    parser.add_argument("--quiet", "-q", help="suppress output", action="store_true")
    args = parser.parse_args()

    if args.list_databases:
        table_data = []
        for name, information in importers.iteritems():
            table_data.append([name, information["description"]])

        print tabulate(table_data, headers=["Name", "Description"])
    else:
        if args.database:
            run_importer(args.database.lower(), args.output_file, args.quiet)
        else:
            for importer_name in importers.iterkeys():
                run_importer(importer_name, args.output_file, args.quiet)


def run_importer(importer_name, output_file, is_quiet):
    if importer_name in importers:
        importer = importers[importer_name]["class"](is_quiet)
        importer.execute(output_file)
    else:
        print "No importer with specified name found!"
        return


if __name__ == "__main__":
    run()

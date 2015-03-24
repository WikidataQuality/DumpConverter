import argparse
from tabulate import tabulate

from dumpconverter.GndDumpConverter import *


# Available dump converter with their key name
importers = {
    "gnd": {
        "class_name": GndDumpConverter,
        "description": "Integrated Authority File of the German National Library."
    }
}


def run():
    # Parse arguments
    parser = argparse.ArgumentParser(description="This program downloads dumps from one or many databases and converts them to CSV data.")
    parser.add_argument("--list-databases", help="list all available databases, that can be imported, and exit", action="store_true")
    parser.add_argument("--database", "-d", help="name of a specific database that should be imported.")
    parser.add_argument("--entities-file", "-e", help="CSV output file for external entities", default="entities.csv")
    parser.add_argument("--meta-file", "-m", help="CSV output file for meta information about the database", default="meta.csv")
    parser.add_argument("--quiet", "-q", help="suppress output", action="store_true")
    args = parser.parse_args()

    if args.list_databases:
        table_data = []
        for name, information in importers.iteritems():
            table_data.append([name, information["description"]])

        print tabulate(table_data, headers=["Name", "Description"])
    else:
        # Open output files
        csv_entities_file = open(args.entities_file, "wb")
        csv_meta_file = open(args.meta_file, "wb")

        # Run requested importer(s)
        if args.database:
            run_importer(args.database.lower(), csv_entities_file, csv_meta_file)
        else:
            for importer_name in importers.iterkeys():
                run_importer(importer_name, csv_entities_file, csv_meta_file, args.quiet)

        # Close file handles
        csv_entities_file.close()
        csv_meta_file.close()


def run_importer(importer_name, csv_entities_file, csv_meta_file, is_quiet):
    if importer_name in importers:
        importer = importers[importer_name]["class_name"](csv_entities_file, csv_meta_file, is_quiet)
        importer.execute()
    else:
        print "No importer with specified name found!"
        return


if __name__ == "__main__":
    run()
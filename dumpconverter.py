"""Main script that executes dump converters depending on parameters"""
import argparse
from tabulate import tabulate

from dumpconverter.DumpConverter import DumpConverter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program downloads dumps from one or many databases and converts them into a format, that can be imported by WikibaseQualityExternalValidation extension.")
    parser.add_argument("--list-databases", help="list all available databases, that can be imported, and exit", action="store_true")
    parser.add_argument("--database", "-d", help="key of a specific database that should be imported.")
    parser.add_argument("--external-values-file", help="CSV output file for data values of dumps.", default="external_values.csv")
    parser.add_argument("--dump-information-file", help="CSV output file for meta informations of dumps.", default="dump_information.csv")
    parser.add_argument("--quiet", "-q", help="suppress output", action="store_true")
    args = parser.parse_args()

    if args.list_databases:
        print tabulate(DumpConverter.get_available_databases(),
                       headers=["Key", "Description"])
    else:
        external_values_file = open(args.external_values_file, "w+b")
        dump_information_file = open(args.dump_information_file, "w+b")

        converter = DumpConverter(external_values_file, dump_information_file, args.database, args.quiet)
        converter.execute()

        external_values_file.close()
        dump_information_file.close()

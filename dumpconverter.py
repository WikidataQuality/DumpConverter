"""Main script that executes dump converters depending on parameters"""
import argparse
from tabulate import tabulate

from dumpconverter.DumpConverter import DumpConverter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program downloads dumps from one or many databases and converts them into a format, that can be imported by WikibaseQualityExternalValidation extension.")
    parser.add_argument("--list-databases", help="list all available databases, that can be imported, and exit", action="store_true")
    parser.add_argument("--database", "-d", help="key of a specific database that should be imported.")
    parser.add_argument("--output-file", "-o", help="TAR output file for data values of dumps.", default="external_data.tar")
    parser.add_argument("--quiet", "-q", help="suppress output", action="store_true")
    args = parser.parse_args()

    if args.list_databases:
        print tabulate(DumpConverter.get_available_databases(),
                       headers=["Key", "Description"])
    else:
        converter = DumpConverter(args.output_file, args.database, args.quiet)
        converter.execute()

import sys
import argparse
from src.ingestion import create_tables, run_ingestion

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Shareholder registry ingestion pipeline and API."
    )

    arg_parser.add_argument(
        "--create-tables",
        required=False,
        action="store_true",
        help="Create tables in the database.",
    )

    arg_parser.add_argument(
        "--ingest",
        required=False,
        action="store_true",
        help="Start the ingestion pipeline to create the database and import the data.",
    )

    arg_parser.add_argument(
        "--years",
        default="2025",
        required=False,
        type=str,
        help="Provide the fiscal years you want to ingest. (Default: 2025)",
    )

    if len(sys.argv) == 1:
        arg_parser.print_help()
        sys.exit(0)

    args = arg_parser.parse_args()

    if args.create_tables:
        create_tables()

    if args.ingest:
        years = args.years.split(",")
        run_ingestion(years)

import argparse

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Shareholder registry ingestion pipeline and API."
    )

    arg_parser.add_argument(
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    arg_parser.add_argument(
        "--ingest",
        required=False,
        type=str,
        help="Start the ingestion pipeline to create the database and import the data.",
    )
    arg_parser.add_argument(
        "--years",
        default="2025",
        required=False,
        type=str,
        help="Provide the fiscal years you want to ingest. (Default: 2025)",
    )

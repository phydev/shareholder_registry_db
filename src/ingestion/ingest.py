import logging

from logger import setup_logger
from src.ingestion.parsers import CSVParser
from client import SQLClient

logger = setup_logger(level=logging.INFO)

def create_tables() -> None:
    """
    create tables in the database
    """
    db_client = SQLClient()
    db_client.create_tables()

def run_ingestion(years: list[str]) -> None:
    """
    run the ingestion pipeline for the fiscal years provided
    """
    for year in years:
        parser = CSVParser(f"data/aksjeeiebok_{year}.csv")

        parser.client.create_tables()

        parser.process_file()

        parser.close_file()

if __name__ == "__main__":
    create_tables()
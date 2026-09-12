import logging

from logger import setup_logger
from src.ingestion.parsers import CSVParser

logger = setup_logger(level=logging.INFO)


if __name__ == "__main__":
    parser = CSVParser("data/aksjeeiebok_2025.csv")

    parser.client.create_tables()

    parser.process_row()

    parser.close_file()

from shareholder_registry.ingestion.ingest import CSVParser

if __name__ == "__main__":

    parser = CSVParser("data/aksjeeiebok_2025.csv")

    parser.client.create_tables()

    parser.process_file()

    parser.close_file()

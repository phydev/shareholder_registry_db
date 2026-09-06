import csv
import re

from models import Company
from src.client import SQLClient
from src.shareholder_registry.models.company import Company
from src.shareholder_registry.models.person import Person
from src.shareholder_registry.models.shareholder import Part
from src.shareholder_registry.models.shares import Shares


class CSVParser:
    def __init__(self,
                 filename: str,
                 delimiter: str = ';'):
        self.filename = filename
        self.fiscal_year = re.search(r'\d{4}', self.filename)
        self.delimiter = delimiter
        self.file = self.open_file()
        self.reader = csv.reader(self.file)
        self.header = next(self.reader)
        self.header_map = self.build_header_map(self.header)
        self.client = self.get_sql_client()

    def get_sql_client(self) -> SQLClient:
        if self.client:
            return self.client
        return SQLClient()

    def process_row(self) -> None:
        row = next(self.reader)
        dict_row = self.read_row(row, self.header_map)
        postnr, sted = dict_row.get("Postnr/sted").split(" ")

        company = Company(
            name=dict_row["Selskap"],
            organization_number=dict_row["OrgNr"],
            shareholder=Part()
        )

        shareholder = Part(postal_code=postnr, city=sted, country_code=dict_row["Landkode"])

        if self.is_person(dict_row):
           part = Person(
                name=dict_row["Navn aksjonær"],
                birth_date=dict_row["Fødselsår/orgnr"],
                shareholder=shareholder,
           )
        else:
           part = Company(name=dict_row["Navn aksjonær"],
                    organization_number=dict_row["Fødselsår/orgnr"],
                             shareholder=shareholder)

        self.client.create_or_update(model=part)
        self.client.create_or_update(model=company)

        shares = Shares(shareholder=shareholder,
                        year=self.fiscal_year,

                        )

    def read_row(self, row: list[str], header_map: dict, delimiter=";") -> dict:
        row = list(row[0].split(delimiter))
        row_dict = {}
        for _n, column in enumerate(header_map):
            row_dict[column] = row[header_map.get(column)]

        return row_dict

    def build_header_map(self, header: list[str]) -> dict:
        """
        Build a map between column names and their respective positions
        for order independent processing.
        """

        header_list = list(header[0].split(';'))

        header_map = {}
        for n, column in enumerate(header_list):
            header_map[column] = n

        return header_map

    def open_file(self):
        return open(self.filename, encoding='utf-8-sig', newline='')

    def close_file(self):
        self.file.close()

    def process_file(self):
        #for row in self.reader:
        #    row_dict = self.process_row(row) # ignore: F841

        self.close_file()

    def is_person(self, row: dict):
        return len(row["Fødselsår/orgnr"]) == 4

if __name__ == '__main__':

    parser = CSVParser('data/aksjeeiebok_2005.csv')

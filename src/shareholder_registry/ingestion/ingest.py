import csv
import re

from src.client import SQLClient
from src.shareholder_registry.models import Company, Person, Part, Shares


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
        self._client: SQLClient | None = None

    @property
    def client(self) -> SQLClient:
        if self._client is None:
            self._client = SQLClient()

        return self._client

    def process_row(self) -> None:
        row = next(self.reader)
        dict_row = self.read_row(row, self.header_map)
        postnr, sted = dict_row.get("Postnr/sted").split(" ")

        if self.is_person(dict_row):
            investor, _ = self.client.create_or_update(model=Person,
                                         lookup_kwargs={"name": dict_row["Navn aksjonær"],
                                                        "birth_date": dict_row["Fødselsår/orgnr"]},
                                         update_values={}
                                         )

        else:
            investor, _ = self.client.create_or_update(
                model=Company,
                lookup_kwargs={"organization_number": dict_row["Fødselsår/orgnr"]},
                update_values={"name": dict_row["Navn aksjonær"]}
            )

        if not investor.id_part:
            part = Part(postal_code=postnr, city=sted, country_code=dict_row["Landkode"])
            investor.part = part
            self.client.session.add(investor)
            self.client.session.commit()
        else:
            self.client.create_or_update(
                model=Part,
                lookup_kwargs={"id": investor.id_part},
                update_values={"postal_code": postnr, "city": sted, "country_code": dict_row["Landkode"]}
            )

        target_company, _ = self.client.create_or_update(
            model=Company,
            lookup_kwargs={"organization_number": dict_row["OrgNr"]},
            update_values={"name": dict_row["Selskap"]}
        )

        if not target_company.id_part:
            target_company.part = Part()
            self.client.session.add(target_company)
            self.client.session.commit()

        self.client.create_or_update(
            model=Shares,
            lookup_kwargs={
                "id_part": investor.id_part,
                "id_company": target_company.id,
                "year": self.fiscal_year,
                "share_class": dict_row.get("Aksjeklasse", "Ordinære aksjer")
            },
            update_values={
                "shares_owned": int(dict_row["Antall aksjer"]),
                "total_shares_in_company": int(dict_row["Total antall aksjer"])
            }
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

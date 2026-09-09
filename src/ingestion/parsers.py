import csv
import logging
import re

from client import SQLClient
from logger import setup_logger
from src.models import Company, Part, Person, Shares

setup_logger()

logger = logging.getLogger(__name__)


class CSVParser:
    def __init__(self, filename: str, delimiter: str = ";"):
        self.filename = filename
        self.fiscal_year = re.search(r"\d{4}", self.filename).group(0)
        self.delimiter = delimiter
        self.file = self.open_file()
        self.reader = csv.reader(self.file, delimiter=self.delimiter)
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

        raw_address_string = dict_row.get("Postnr/sted", "")
        parsed_address, needs_review = parse_address(raw_address_string)

        # Log a warning for manual review if the data was corrupted
        if needs_review:
            logger.warning(
                f"⚠️ Corrupted address flagged for review! "
                f"OrgNr/ID: {dict_row.get('Fødselsår/orgnr')} | "
                f"Cleaned: {parsed_address} | "
                f"Original Raw Input: '{raw_address_string}'"
            )

        postal_code, location = (
            parsed_address["postal_code"],
            parsed_address["location"],
        )

        if self.is_person(dict_row):
            investor, _ = self.client.create_or_update(
                model=Person,
                lookup_kwargs={
                    "name": dict_row["Navn aksjonær"],
                    "birth_year": dict_row["Fødselsår/orgnr"],
                },
                update_values={},
            )
        else:
            investor, _ = self.client.create_or_update(
                model=Company,
                lookup_kwargs={"organization_number": dict_row["Fødselsår/orgnr"]},
                update_values={"name": dict_row["Navn aksjonær"]},
            )

        if not investor.part:
            investor.part = Part(
                postal_code=postal_code,
                location=location,
                country_code=dict_row["Landkode"],
            )
        else:
            investor.part.postal_code = postal_code
            investor.part.location = location
            investor.part.country_code = dict_row["Landkode"]

        # check if the investor and the target company are the same entity
        if (
            not self.is_person(dict_row)
            and dict_row["Orgnr"] == dict_row["Fødselsår/orgnr"]
        ):
            target_company = investor

            target_company.name = dict_row["Selskap"]
        else:
            target_company, _ = self.client.create_or_update(
                model=Company,
                lookup_kwargs={"organization_number": dict_row["Orgnr"]},
                update_values={"name": dict_row["Selskap"]},
            )

        if not target_company.part:
            target_company.part = Part()

        shares, _ = self.client.create_or_update(
            model=Shares,
            lookup_kwargs={
                "part": investor.part,
                "company": target_company,
                "year": self.fiscal_year,
                "share_class": dict_row.get("Aksjeklasse", "Ordinære aksjer"),
            },
            update_values={
                "shares_owned": int(dict_row["Antall aksjer"]),
                "total_shares_in_company": int(dict_row["Antall aksjer selskap"]),
            },
        )

        self.client.session.add(shares)
        self.client.session.commit()

    def read_row(self, row: list[str], header_map: dict, delimiter=";") -> dict:
        # row = list(row[0].split(delimiter))
        logger.info(f"Processing row: {row}")
        row_dict = {}
        for _n, column in enumerate(header_map):
            row_dict[column] = row[header_map.get(column)]

        return row_dict

    def build_header_map(self, header: list[str]) -> dict:
        """
        Build a map between column names and their respective positions
        for order independent processing.
        """

        header_map = {}
        for n, column in enumerate(header):
            header_map[column] = n

        logger.info(f"Building header_map: {header_map}")
        return header_map

    def open_file(self):
        return open(self.filename, encoding="utf-8-sig", newline="")

    def close_file(self):
        self.file.close()

    def process_file(self) -> None:
        for _ in self.reader:
            self.process_row()  # ignore: F841

        self.close_file()

    def is_person(self, row: dict):
        return len(row["Fødselsår/orgnr"]) == 4


def parse_address(address: str) -> tuple[dict, bool]:
    parsed_address = {"postal_code": None, "location": None}
    needs_review = False

    address = address.strip().strip("\"'")
    if not address:
        return parsed_address, needs_review

    all_codes = re.findall(r"\d+", address)
    if all_codes:
        parsed_address["postal_code"] = all_codes[0]
        if len(set(all_codes)) > 1:
            needs_review = True

    text_only = re.sub(r"\d+", " ", address)

    text_only = re.sub(r"\s+,\s*", ", ", text_only)

    words = text_only.split()
    seen = set()
    unique_words = []

    for word in words:
        word_clean = word.upper().strip(" ,")
        if not word_clean:
            continue

        if word_clean not in seen:
            seen.add(word_clean)
            unique_words.append(word)
        else:
            needs_review = True

    if unique_words:
        location = " ".join(unique_words).strip()
        location = re.sub(r"\s+,\s*", ", ", location)
        parsed_address["location"] = location
    else:
        parsed_address["location"] = None

    return parsed_address, needs_review

"""
CSV -> DuckLake ingestion.

Each table's shape lives in its own schema file (schemas/orders.py,
schemas/customers.py, ...). This module just wires them together:
connect, create the table from its schema, validate + load the CSV,
insert. No SQL string is built anywhere except the two one-liners below.
"""

import duckdb
import pandas as pd

from config import DATA_PATH, POSTGRES_CONN
from schemas import ALL_SCHEMAS
from schemas.base import LakeSchema


def get_connection() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.install_extension("ducklake")
    con.install_extension("postgres")
    con.load_extension("ducklake")
    con.load_extension("postgres")
    con.sql(
        f"ATTACH 'ducklake:postgres:{POSTGRES_CONN}' AS my_lake "
        f"(DATA_PATH '{DATA_PATH}')"
    )
    con.sql("USE my_lake")
    return con


def create_table_if_not_exists(con: duckdb.DuckDBPyConnection, schema: type[LakeSchema]) -> None:
    con.sql(f"CREATE TABLE IF NOT EXISTS {schema.table_name} ({schema.ddl_columns()})")


def load_and_validate(schema: type[LakeSchema]) -> pd.DataFrame:
    """Read the CSV and validate every row against its Pydantic model."""
    raw_rows = pd.read_csv(schema.csv_path).to_dict(orient="records")
    validated = [schema(**row).model_dump() for row in raw_rows]
    return pd.DataFrame(validated)


def ingest(con: duckdb.DuckDBPyConnection, schema: type[LakeSchema]) -> None:
    create_table_if_not_exists(con, schema)
    df = load_and_validate(schema)
    con.sql("SELECT * FROM df").insert_into(schema.table_name)
    count = con.sql(f"SELECT COUNT(*) FROM {schema.table_name}").fetchone()[0]
    print(f"[{schema.table_name}] now has {count} rows")


def main() -> None:
    con = get_connection()
    for schema in ALL_SCHEMAS:
        ingest(con, schema)
    con.close()


if __name__ == "__main__":
    main()

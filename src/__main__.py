from sqlmodel import SQLModel, create_engine

from settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}")

def main() -> None:
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    main()

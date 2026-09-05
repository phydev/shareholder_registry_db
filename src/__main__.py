from sqlmodel import SQLModel, create_engine

from settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

def main() -> None:
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    main()

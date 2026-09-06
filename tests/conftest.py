from collections.abc import Generator
import pytest
from sqlmodel import SQLModel, Session, create_engine
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session", autouse=True)
def postgres_container(request: pytest.FixtureRequest) -> PostgresContainer:
    """Spins up a clean Postgres testcontainer once per test session."""
    # We use a standard stable image tags for reliable local execution
    postgres = PostgresContainer(image="postgres:16-alpine")

    postgres.start()

    # Ensures the container is cleanly torn down when pytest finishes
    request.addfinalizer(postgres.stop)
    return postgres


@pytest.fixture(name="session")
def session_fixture(postgres_container: PostgresContainer) -> Generator[Session, None, None]:
    """Creates a new SQLModel session connected to the active local container."""
    # Dynamically gets the URL with the randomized port assigned by your Mac's Docker
    connection_url = postgres_container.get_connection_url()

    engine = create_engine(connection_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

import logging
from functools import cached_property
from typing import Any, TypeVar

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from src.logging import setup_logger

setup_logger()

# 2. Get a standard logger for this file
logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=SQLModel)


class SQLClient:
    def __init__(self):
        self._session: Session | None = None
        self._engine: Engine | None = None
        self._session: Session | None = None

    @cached_property
    def db_address(self):
        return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    def engine(self) -> Engine:
        if self._engine is None:
            logger.info(f"Creating engine for {self.db_address}")
            self._engine = create_engine(self.db_address)

        return self._engine

    def session(self) -> Session:
        if self._session is None:
            logger.info(f"Creating session for {self.db_address}")
            self._session = Session(bind=self.engine)

        return self._session


    def create_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_or_create(
            self,
            model: type[ModelType],
            defaults: dict[str, Any] | None = None,
            **kwargs: Any
    ) -> tuple[ModelType, bool]:
        statement = select(model).filter_by(**kwargs)
        instance = self.session.exec(statement).first()

        if instance:
            return instance, False

        params = {**kwargs, **(defaults or {})}
        instance = model(**params)

        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance, True

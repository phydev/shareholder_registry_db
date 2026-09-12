import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .company import Company
    from .person import Person
    from .shares import Shares


class Part(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PostgresUUID(as_uuid=True), primary_key=True),
    )

    postal_code: str = Field(
        max_length=10, description=("Postal code for part"), nullable=True
    )
    location: str = Field(
        ..., max_length=100, description="Location of the part", nullable=True
    )
    country_code: str = Field(
        ..., max_length=3, description="Country code", nullable=True
    )

    investments: list["Shares"] = Relationship(back_populates="part")

    as_person: Optional["Person"] = Relationship(back_populates="part")
    as_company: Optional["Company"] = Relationship(back_populates="part")

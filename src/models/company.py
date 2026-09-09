import uuid
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlmodel import Column, Field, ForeignKey, Relationship, SQLModel

if TYPE_CHECKING:
    from .shares import Shares


class Company(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PostgresUUID(as_uuid=True), primary_key=True)
    )

    id_part: uuid.UUID = Field(
        sa_column=Column(
            PostgresUUID(as_uuid=True),
            ForeignKey("part.id"),
            nullable=False
        )
    )

    name: str = Field(..., max_length=255, description="Name of the company")

    organization_number: str = Field(
        ..., max_length=9, description="Organization number", unique=True
    )

    part: "Part" = Relationship(back_populates="as_company") # noqa: F821

    shareholders: list["Shares"] = Relationship(back_populates="company") # noqa: F821

import uuid
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .shares import Shares


class Company(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_part: UUID = Field(
        default_factory=uuid.uuid4, nullable=False, foreign_key="part.id"
    )

    name: str = Field(..., max_length=255, description="Name of the company")

    organization_number: str = Field(
        ..., max_length=9, description="Organization number", unique=True
    )

    part: "Part" = Relationship(back_populates="as_company") # noqa: F821

    shareholders: list["Shares"] = Relationship(back_populates="company") # noqa: F821

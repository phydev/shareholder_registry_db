import uuid
from uuid import UUID

from typing import List, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .shares import Shares

class Company(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_part: UUID = Field(default_factory=uuid.uuid4, nullable=False, foreign_key="part.id")

    name: str = Field(
        ..., max_length=255, description="Name of the company"
    )

    organization_number: str = Field(
        ..., max_length=9, description="Organization number", unique=True
    )

    part: "Part" = Relationship(back_populates="as_company")

    shareholders: List["Shares"] = Relationship(back_populates="company")

import uuid
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .company import Company
    from .person import Person
    from .shares import Shares


class Part(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    postal_code: str = Field(
        max_length=10, description=("Postal code for part"), nullable=True
    )
    city: str = Field(
        ..., max_length=100, description="City of the part", nullable=True
    )
    country_code: str = Field(
        ..., max_length=3, description="Country code", nullable=True
    )

    investments: list["Shares"] = Relationship(back_populates="part")

    as_person: Optional["Person"] = Relationship(back_populates="part")
    as_company: Optional["Company"] = Relationship(back_populates="part")

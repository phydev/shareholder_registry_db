import uuid
from uuid import UUID
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .shares import Shares
    from .person import Person
    from .company import Company


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

    investments: List["Shares"] = Relationship(back_populates="part")

    as_person: Optional["Person"] = Relationship(back_populates="part")
    as_company: Optional["Company"] = Relationship(back_populates="part")

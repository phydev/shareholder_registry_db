import uuid
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class Person(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("name", "birth_year", name="uq_person_name_birth_year"),
    )

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_part: UUID = Field(
        default_factory=uuid.uuid4, nullable=False, foreign_key="part.id"
    )

    name: str = Field(..., max_length=255, description="Name of the shareholder")
    birth_year: str = Field(
        ...,
        max_length=9,
        description=("Birth year for shareholders identified in the National Registry"),
    )

    part: "Part" = Relationship(back_populates="as_person")

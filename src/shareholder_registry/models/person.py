import uuid

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlmodel import Column, Field, Relationship, SQLModel, UniqueConstraint, ForeignKey


class Person(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("name", "birth_year", name="uq_person_name_birth_year"),
    )

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

    name: str = Field(..., max_length=255, description="Name of the shareholder")
    birth_year: str = Field(
        ...,
        max_length=9,
        description=("Birth year for shareholders identified in the National Registry"),
    )

    part: "Part" = Relationship(back_populates="as_person") # noqa: F821

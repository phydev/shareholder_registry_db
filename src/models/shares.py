import uuid

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlmodel import BigInteger, Column, Field, ForeignKey, Relationship, SQLModel


class Shares(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PostgresUUID(as_uuid=True), primary_key=True),
    )

    id_part: uuid.UUID = Field(
        sa_column=Column(
            PostgresUUID(as_uuid=True), ForeignKey("part.id"), nullable=False
        )
    )
    id_company: uuid.UUID = Field(
        sa_column=Column(
            PostgresUUID(as_uuid=True), ForeignKey("company.id"), nullable=False
        )
    )

    year: str = Field(max_length=4)
    share_class: str = Field(max_length=100)
    shares_owned: int = Field(sa_column=Column(BigInteger))
    total_shares_in_company: int = Field(sa_column=Column(BigInteger))

    part: "Part" = Relationship(back_populates="investments")  # noqa: F821
    company: "Company" = Relationship(back_populates="shareholders")  # noqa: F821

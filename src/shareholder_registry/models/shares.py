import uuid
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger


class Shares(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_part: UUID = Field(foreign_key="part.id", nullable=False)
    id_company: UUID = Field(foreign_key="company.id", nullable=False)

    year: str = Field(max_length=4)
    share_class: str = Field(max_length=100)
    shares_owned: int = Field(sa_column=Column(BigInteger))
    total_shares_in_company: int = Field(sa_column=Column(BigInteger))

    part: "Part" = Relationship(back_populates="investments") # noqa: F821
    company: "Company" = Relationship(back_populates="shareholders") # noqa: F821

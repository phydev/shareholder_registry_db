import uuid
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class Shares(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_part: UUID = Field(foreign_key="part.id", nullable=False)
    id_company: UUID = Field(foreign_key="company.id", nullable=False)

    year: str = Field(max_length=4)
    share_class: str = Field(max_length=100)
    shares_owned: int
    total_shares_in_company: int

    part: "Part" = Relationship(back_populates="investments")
    company: "Company" = Relationship(back_populates="shareholders")

import uuid
from uuid import UUID
from sqlmodel import Field, SQLModel, Date
from datetime import date

class Shares(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_shareholder: UUID = Field(foreign_key="Shareholder.id")

    id_company: UUID = Field(default_factory=uuid.uuid4, foreign_key="Company.id")

    year: date.year = Field(description="Snaptshot year")

    share_class: str = Field(
        ..., max_length=100, description="Share class or ISIN for the share class"
    )
    shares_owned: int = Field(
        ..., description="Number of shares at the end of the income year"
    )
    total_shares_in_company: int = Field(
        ..., description="Total number of shares in the company"
    )
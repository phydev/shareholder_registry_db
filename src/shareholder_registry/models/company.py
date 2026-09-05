import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field

class Company(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4)
    id_shareholder: UUID = Field(default_factory=uuid.uuid4, nullable=False, foreign_key="Shareholder.id")

    name: str = Field(
        ..., max_length=255, description="Name of the company"
    )

    organization_number: str = Field(
        ..., max_length=20, description="Organization number"
    )
    postal_code: str = Field(
        ...,
        max_length=100,
        description=(
            "Postal code for shareholder"
        ),
    )
    city: str = Field(..., max_length=100, description="City of the shareholder")
    country_code: str = Field(..., max_length=3, description="Country code")

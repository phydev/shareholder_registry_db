import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field

class Shareholder(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4)
    postal_code: str = Field(max_length=4, description=("Postal code for shareholder"), null=True)
    city: str = Field(..., max_length=100, description="City of the shareholder")
    country_code: str = Field(..., max_length=3, description="Country code")


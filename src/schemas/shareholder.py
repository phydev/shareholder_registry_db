from enum import StrEnum

from pydantic import BaseModel, computed_field


class PartType(StrEnum):
    person = "person"
    company = "company"


class ShareholderOut(BaseModel):
    name: str
    owner_type: PartType
    shares_owned: int
    total_shares_in_company: int

    @computed_field
    def ownership_fraction(self) -> float:
        """
        Calculates the fraction of total company shares owned by this entity.
        Returns a float between 0.0 and 1.0 (e.g., 0.25 for 25%).
        """
        if self.total_shares_in_company == 0:
            return 0.0
        return self.shares_owned / self.total_shares_in_company


class CompanyOwnershipResponse(BaseModel):
    organization_number: str
    company_name: str
    shareholders: list[ShareholderOut]

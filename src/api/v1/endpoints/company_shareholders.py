from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from src.client import SQLClient
from src.models import Company, Shares
from src.schemas.shareholder import CompanyOwnershipResponse, ShareholderOut

ownership_router = APIRouter()


@ownership_router.get(
    "/company/{organization_number}/owners", response_model=CompanyOwnershipResponse
)
def get_company_owners(organization_number: str, db: SQLClient = Depends(SQLClient)):
    """
    Publicly accessible endpoint to fetch all owners/shareholders of a company
    along with their calculated fractional ownership.
    """

    company_stmt = select(Company).where(
        Company.organization_number == organization_number
    )
    company = db.session.exec(company_stmt).first()

    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company not found: {organization_number}"
        )

    shares_stmt = select(Shares).where(Shares.id_company == company.id)
    shares_records = db.session.exec(shares_stmt).all()

    shareholders_list = []
    for share in shares_records:
        part_record = share.part

        if getattr(part_record, "as_person", None):
            name = part_record.as_person.name
            owner_type = "person"
        else:
            name = part_record.as_company.name
            owner_type = "company"

        shareholder_data = ShareholderOut(
            name=name,
            owner_type=owner_type,
            shares_owned=share.shares_owned,
            total_shares_in_company=share.total_shares_in_company,
        )
        shareholders_list.append(shareholder_data)

    return CompanyOwnershipResponse(
        organization_number=company.organization_number,
        company_name=company.name,
        shareholders=shareholders_list,
    )

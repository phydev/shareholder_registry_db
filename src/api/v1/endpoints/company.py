from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from src.client import SQLClient
from src.models import Company

company_router = APIRouter(prefix="/company", tags=["Company"])


@company_router.get("/{organization_number}", response_model=Company)
def read_company(organization_number: str, db: SQLClient = Depends(SQLClient)):
    """
    Publicly accessible endpoint to fetch a single record.
    """
    statement = select(Company).where(
        Company.organization_number == organization_number
    )
    company = db.session.exec(statement).first()
    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company not found: {organization_number}"
        )
    return company

@company_router.post("/", response_model=list[Company])
def list_companies(db: SQLClient = Depends(SQLClient)):
    """
    List all companies in the registry
    """
    statement = select(Company)

    companies = db.session.exec(statement).all()

    return companies

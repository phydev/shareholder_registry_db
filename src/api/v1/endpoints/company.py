from fastapi import APIRouter, Depends, HTTPException

from src.client import SQLClient
from sqlmodel import select
from src.models import Company

company_router = APIRouter()

@company_router.get("/company/{organization_number}", response_model=Company)
def read_company(organization_number: str, db: SQLClient = Depends(SQLClient)):
    """
    Publicly accessible endpoint to fetch a single record.
    """
    statement = select(Company).where(Company.organization_number == organization_number)
    company = db.session.exec(statement).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company not found: {organization_number}")
    return company

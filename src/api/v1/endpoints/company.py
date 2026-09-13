from fastapi import APIRouter, Depends, Query, HTTPException
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

@company_router.get("/", response_model=list[Company])
def list_companies(db: SQLClient = Depends(SQLClient),
                   offset: int = 0,
                   limit: int = Query(default=100, le=100)):
    """
    List all companies in the registry
    """
    statement = select(Company).offset(offset).limit(limit)

    companies = db.session.exec(statement).all()

    return companies

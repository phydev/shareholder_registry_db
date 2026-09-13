from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from src.api.schemas import PartType
from src.client import SQLClient
from src.models import Company, Person, Shares

part_route = APIRouter(prefix="/part", tags=["Part"])


@part_route.get("/search/{name}")
def search_shareholder(
        name: str,
        part_type: PartType,
        db: SQLClient = Depends(SQLClient)
):
    """
    Search part by name.
    """

    part_entity = Person if part_type.value == 'person' else Company

    query = select(part_entity).where(part_entity.name.contains(name))

    results = db.session.exec(query).all()

    return results


@part_route.get("/search/{name}/shares")
def search_shareholder_shares(
        name: str,
        part_type: PartType,
        db: SQLClient = Depends(SQLClient)
):
    """
    Fetch all shares owned by all parts that match the search criteria.
    """

    part_entity = Person if part_type.value == 'person' else Company

    query = (
        select(Shares)
        .join(part_entity, Shares.id_part == part_entity.id_part)
        .where(part_entity.name.contains(name))
    )

    results = db.session.exec(query).all()

    return results




@part_route.get("/{id_part}/shares")
def shares_part(id_part: UUID, db: SQLClient = Depends(SQLClient)):
    """
    Fetch all shares owned by a part.
    """
    query = select(Shares).where(
       Shares.id_part == id_part
    )

    # TODO: maybe implement a join and return company name, orgnr, etc?
    # define a schema
    #shares = db.session.exec(query).all()

    #query = query.join(Company, Company.id == Shares.id_company)

    results = db.session.exec(query).all()

    if not results:
        raise HTTPException(
            status_code=404, detail=f"Part not found: {id_part}"
        )
    return results


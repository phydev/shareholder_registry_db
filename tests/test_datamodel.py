from sqlmodel import Session, select
from src.models import Company, Part, Person, Shares


def test_model_consistency_and_relationships(session: Session):
    # 1. Arrange: Create a Target Company (the asset being owned)
    # It must have a backing 'Part' identity envelope
    target_company_part = Part(postal_code=None, location=None, country_code=None)
    target_company = Company(
        name="Target AS",
        organization_number="123456789",
        part=target_company_part
    )
    session.add(target_company)
    session.commit()  # Flushes IDs to SQLite

    # 2. Arrange: Create an individual Investor (Person)
    investor_person_part = Part(postal_code="0484", location="Oslo", country_code="NO")
    investor_person = Person(
        name="Ola Nordmann",
        birth_year="1985",
        part=investor_person_part
    )
    session.add(investor_person)

    # 3. Arrange: Create a corporate Investor (Company)
    investor_company_part = Part(postal_code="5000", location="Bergen", country_code="NO")
    investor_company = Company(
        name="Holding AS",
        organization_number="987654321",
        part=investor_company_part
    )
    session.add(investor_company)
    session.commit()

    # 4. Arrange: Create Share transactions linking investors to the Target Company
    shares1 = Shares(
        id_part=investor_person_part.id,
        id_company=target_company.id,
        year="2025",
        share_class="A",
        shares_owned=60,
        total_shares_in_company=100
    )
    shares2 = Shares(
        id_part=investor_company_part.id,
        id_company=target_company.id,
        year="2025",
        share_class="A",
        shares_owned=40,
        total_shares_in_company=100
    )
    session.add_all([shares1, shares2])
    session.commit()

    # Clear the session cache to force reloading clean records from SQLite
    session.expire_all()

    # ----------------------------------------------------
    # ASSERTIONS: Testing Model Consistency & Back-references
    # ----------------------------------------------------

    # Query the target company from the database
    db_company = session.exec(select(Company).where(Company.organization_number == "123456789")).one()

    # Check 1: Does the target company know who its shareholders are via 'Shares'?
    assert len(db_company.shareholders) == 2

    # Check 2: Verify polymorphic attributes (Identity Resolution)
    # Sort shareholders by shares owned so we can cleanly test individual vs corporate
    sorted_shares = sorted(db_company.shareholders, key=lambda s: s.shares_owned, reverse=True)

    # The 60-share block belongs to Ola Nordmann (Person)
    person_share_record = sorted_shares[0]
    assert person_share_record.part.as_person is not None
    assert person_share_record.part.as_person.name == "Ola Nordmann"
    assert person_share_record.part.as_company is None  # Should be mutually exclusive
    assert person_share_record.part.location == "Oslo"  # Check address on the envelope

    # The 40-share block belongs to Holding AS (Company)
    company_share_record = sorted_shares[1]
    assert company_share_record.part.as_company is not None
    assert company_share_record.part.as_company.name == "Holding AS"
    assert company_share_record.part.as_person is None  # Should be mutually exclusive
    assert company_share_record.part.location == "Bergen"

    # Check 3: Reverse lookup (Investor -> Investments)
    db_person_part = session.exec(select(Part).where(Part.id == investor_person_part.id)).one()
    assert len(db_person_part.investments) == 1
    assert db_person_part.investments[0].company.name == "Target AS"

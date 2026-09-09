from fastapi import FastAPI

app = FastAPI(
    title="Shareholder registry API",
    description="Retrieve shareholders and companies from the registry",
    summary="Read-only API.",
    version="0.0.1",
    terms_of_service="Check the MIT license.",
    contact={
        "name": "Mauricio Moreira Soares",
        "url": "http://phydev.github.io",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit",
    },
)

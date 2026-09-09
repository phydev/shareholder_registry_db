from fastapi import FastAPI

from src.api.v1.endpoints import company_router, ownership_router

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


@app.get("/")
async def root():
    return {
        "message": (
            "Aksjonærregisteret API is up and running!"
            " For documentation access /docs"
            " (Swagger UI) or /redoc (ReDoc)"
        )
    }


app.include_router(company_router)
app.include_router(ownership_router)

if __name__ == "__main__":
    # run rest api with uvicorn
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

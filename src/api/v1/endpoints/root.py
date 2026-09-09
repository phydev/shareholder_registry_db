from fastapi import APIRouter

root_router = APIRouter()

@root_router.get("/")
async def root():
    return {
        "message": (
            "Shareholder registry API is up and running!"
            " For documentation access /docs"
            " (Swagger UI) or /redoc (ReDoc)"
        )
    }


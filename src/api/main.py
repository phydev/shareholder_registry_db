import uvicorn

from src.api.config import app
from src.api.v1.endpoints import company_router, company_shareholder_router, part_route, root_router

app.include_router(root_router)
app.include_router(company_router)
app.include_router(company_shareholder_router)
app.include_router(part_route)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

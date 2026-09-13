from .company import company_router
from .company_shareholders import company_shareholder_router
from .part import part_route
from .root import root_router

__all__ = [
    "root_router",
    "company_router",
    "part_route",
    "company_shareholder_router",
]

"""Operational health-check routes."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def create_health_router(engine: Engine) -> APIRouter:
    """Create health routes that verify database availability."""
    router = APIRouter(tags=["health"])

    @router.get("/health")
    def get_health() -> JSONResponse:
        """Report whether the API and configured database are available."""
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unhealthy", "database": "unreachable"},
            )

        return JSONResponse(content={"status": "healthy", "database": "reachable"})

    return router

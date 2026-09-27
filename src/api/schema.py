"""API routes for inspecting the schema used by the text-to-SQL agent."""

from fastapi import APIRouter
from sqlalchemy.engine import Engine

from src.database.schemas import schema_table


def create_schema_router(engine: Engine) -> APIRouter:
    """Create schema inspection routes backed by the agent's database engine."""
    router = APIRouter()

    @router.get("/schema", tags=["schema"])
    def get_database_schema() -> dict[str, list[str]]:
        """Return table and column names in the format provided to the agent."""
        return schema_table(engine)

    return router

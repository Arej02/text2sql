"""API routes for inspecting the schema used by the text-to-SQL agent."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from src.database.schemas import schema_table


def create_schema_router(engine: Engine) -> APIRouter:
    """Create schema inspection routes backed by the agent's database engine."""
    router = APIRouter()

    @router.get("/schema", tags=["schema"])
    def get_database_schema() -> dict[str, list[str]]:
        """Return table and column names in the format provided to the agent."""
        return schema_table(engine)

    @router.get("/tables/{table_name}", tags=["schema"])
    def get_table_details(table_name: str) -> dict:
        """Return column metadata and primary-key information for one table."""
        database_inspector = inspect(engine)
        if table_name not in database_inspector.get_table_names():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' was not found.",
            )

        columns = []
        for column in database_inspector.get_columns(table_name):
            columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column.get("nullable"),
                "default": column.get("default"),
            })

        primary_key = database_inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        return {
            "table_name": table_name,
            "columns": columns,
            "primary_key": primary_key,
        }

    return router

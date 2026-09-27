from sqlalchemy import create_engine

from src.database.db_connection import query_db


def test_query_db_returns_rows_and_execution_time():
    engine = create_engine("sqlite://")

    rows, execution_time_ms = query_db("SELECT 1 AS value", engine)

    assert [dict(row) for row in rows] == [{"value": 1}]
    assert isinstance(execution_time_ms, float)
    assert execution_time_ms >= 0

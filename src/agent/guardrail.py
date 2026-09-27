import sqlparse
import re
import os


def _max_query_rows() -> int:
    """Read and validate the configured maximum row count."""
    value = os.getenv("MAX_QUERY_ROWS", "10")
    try:
        maximum = int(value)
    except ValueError as exc:
        raise ValueError("MAX_QUERY_ROWS must be a positive integer.") from exc
    if maximum < 1:
        raise ValueError("MAX_QUERY_ROWS must be a positive integer.")
    return maximum

def check_select_only(sql_query: str):
    statements = sqlparse.parse(sql_query)
    if not statements:
        return False
    return statements[0].get_type().upper() == "SELECT"

def enforce_limit(sql_query: str, default_limit: int = 10):
    if "limit" in sql_query.lower():
        return sql_query
    return sql_query.rstrip(";") + f" LIMIT {default_limit}"

def reject_invalid_count(sql_query: str):
    if re.search(r"\bcount\s+[a-zA-Z_*]", sql_query, re.IGNORECASE):
        raise ValueError("COUNT must use parentheses, e.g. COUNT(column)")

def validate_sql(sql_query: str) -> str:
    if not check_select_only(sql_query):
        raise ValueError("Only SELECT statements are allowed.")
    reject_invalid_count(sql_query)
    max_rows = _max_query_rows()
    query = enforce_limit(sql_query, default_limit=max_rows)
    limit_match = re.search(r"\bLIMIT\s+(-?\d+)\b", query, re.IGNORECASE)
    if limit_match and not 1 <= int(limit_match.group(1)) <= max_rows:
        query = query[:limit_match.start(1)] + str(max_rows) + query[limit_match.end(1):]
    return query

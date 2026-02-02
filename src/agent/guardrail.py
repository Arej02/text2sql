import sqlparse
import re

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
    return enforce_limit(sql_query)

import sqlparse

def check_select_only(sql_query: str):
    statements = sqlparse.parse(sql_query)
    if not statements:
        return False
    return statements[0].get_type().upper() == "SELECT"

def enforce_limit(sql_query: str, default_limit: int = 10):
    if "limit" in sql_query.lower():
        return sql_query
    return sql_query.rstrip(";") + f" LIMIT {default_limit}"

def validate_sql(sql_query: str) -> str:
    if not check_select_only(sql_query):
        raise ValueError("Only SELECT statements are allowed.")
    return enforce_limit(sql_query)

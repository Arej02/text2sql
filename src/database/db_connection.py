from sqlalchemy import text

def query_db(sql_query,engine):
    sql_query=sql_query.strip()

    try:
        with engine.connect() as conn:
            result=conn.execute(text(sql_query))
            if result.returns_rows:
                rows=list(result.mappings())
                return rows
            return []
    except Exception as e:
        print("Query failed",str(e))
        return []

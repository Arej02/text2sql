from sqlalchemy import text
from time import perf_counter

def query_db(sql_query,engine):
    sql_query=sql_query.strip()

    try:
        with engine.connect() as conn:
            start_time = perf_counter()
            result=conn.execute(text(sql_query))
            if result.returns_rows:
                rows=list(result.mappings())
                return rows, round((perf_counter() - start_time) * 1000, 3)
            return [], round((perf_counter() - start_time) * 1000, 3)
    except Exception as e:
        print("Query failed",str(e))
        return [], 0.0

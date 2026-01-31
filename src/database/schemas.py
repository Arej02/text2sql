from sqlalchemy import inspect

def schema_table(engine):
    insp=inspect(engine)
    table_names=insp.get_table_names() 
    schema_dict={}

    for table_name in table_names:
        columns_info=insp.get_columns(table_name)
        column_names=[col["name"] for col in columns_info]
        schema_dict[table_name]=column_names

    return schema_dict








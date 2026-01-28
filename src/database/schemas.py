from sqlalchemy import inspect

# Returns the schema of all the tables as a dictionary
def schema_table(engine):
    insp=inspect(engine)
    table_names=insp.get_table_names() 
    features=insp.get_columns(table_names[0]) 
    new_dict={}
    for table in table_names:
        new_list=[]
        for col in features:
            col_name=col.get("name")
            new_list.append(col_name)
        new_dict[table]=new_list
    return new_dict







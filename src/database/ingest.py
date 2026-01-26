import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_PATH=Path(__file__).resolve().parent.parent.parent
print(BASE_PATH)
FOLDER_PATH=BASE_PATH/"data"

def normalize_file(file_name:Path):
    return file_name.stem.lower().strip()
    
def normalize_columns(df:pd.DataFrame):
    df_copy=df.copy()
    df_copy.columns=df_copy.columns.str.strip().str.lower().str.replace("-","_").str.replace(" ","_")
    return df_copy

def ingest(folder_path:Path):
    conn_string="sqlite:///./test.db"
    engine=create_engine(conn_string)

    for file in folder_path.iterdir():
        if file.suffix==".csv":
            file_name=normalize_file(file)
            df=pd.read_csv(file)
            df=normalize_columns(df)
            df.to_sql(file_name,engine,index=False,if_exists="replace")

    print("Successfully converted into tables")





    




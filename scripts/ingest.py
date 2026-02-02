import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import argparse

BASE_PATH=Path(__file__).resolve().parent.parent
print(BASE_PATH)
FOLDER_PATH=BASE_PATH/"data"

def normalize_file(file_name:Path):
    return file_name.stem.lower().strip()
    
def normalize_columns(df:pd.DataFrame):
    df_copy=df.copy()
    df_copy.columns=df_copy.columns.str.strip().str.lower().str.replace("-","_").str.replace(" ","_")
    return df_copy

def ingest_files(folder_path:Path,database_path:Path):
    engine=create_engine(database_path)

    if not folder_path.exists() or not folder_path.is_dir():
        raise FileExistsError("The folder doesnot exist")
    
    csv_list=list(folder_path.glob("*.csv"))
    if not csv_list:
        raise FileExistsError("No CSV files found")

    for file in folder_path.iterdir():
        if file.suffix==".csv":
            file_name=normalize_file(file)
            df=pd.read_csv(file)
            df=normalize_columns(df)
            df.to_sql(file_name,engine,index=False,if_exists="replace")

    print("Successfully converted into tables")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("folder_path",help="Enter your folder path")
    parser.add_argument("database_path",help="Enter your database path (e.g., sqlite:///./test.db)")
    args=parser.parse_args()

    folder=Path(args.folder_path)
    ingest(folder,args.database_path)


    




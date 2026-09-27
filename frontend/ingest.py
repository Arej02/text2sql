import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import argparse
import os
import re
from collections import Counter
from collections.abc import Iterable

DEFAULT_MAX_CSV_FILE_SIZE_MB = 10

BASE_PATH=Path(__file__).resolve().parent.parent
print(BASE_PATH)
FOLDER_PATH=BASE_PATH/"data"


def get_max_csv_file_size_bytes() -> int:
    """Return the configured upload limit in bytes."""
    value = os.getenv("MAX_CSV_FILE_SIZE_MB", str(DEFAULT_MAX_CSV_FILE_SIZE_MB))
    try:
        size_mb = float(value)
    except ValueError as exc:
        raise ValueError("MAX_CSV_FILE_SIZE_MB must be a positive number.") from exc

    if size_mb <= 0:
        raise ValueError("MAX_CSV_FILE_SIZE_MB must be a positive number.")

    return int(size_mb * 1024 * 1024)


def validate_uploaded_files(files: Iterable) -> list[str]:
    """Return validation errors for a batch of Streamlit uploaded CSV files."""
    uploaded_files = list(files)
    file_names = [Path(file.name).name for file in uploaded_files]
    duplicate_names = {
        name for name, count in Counter(name.casefold() for name in file_names).items()
        if count > 1
    }
    max_size_bytes = get_max_csv_file_size_bytes()
    errors = []

    for file, file_name in zip(uploaded_files, file_names):
        file_size = file.size
        if file_name.casefold() in duplicate_names:
            errors.append(f"{file_name}: duplicate filename in this upload.")
        if file_size == 0:
            errors.append(f"{file_name}: file is empty.")
        elif file_size > max_size_bytes:
            errors.append(
                f"{file_name}: exceeds the {max_size_bytes / 1024 / 1024:g} MB upload limit."
            )

    return errors

def normalize_file(file_name: Path) -> str:
    name = file_name.stem.lower().strip()
    name = re.sub(r'[^a-z0-9_]', '_', name)      
    name = re.sub(r'_+', '_', name)              
    name = name.strip('_')                       
    
    if not name or name[0].isdigit():
        name = f"t_{name}"                      
    
    return name

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[^a-z0-9_]', '_', regex=True)
    )
    return df

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
    ingest_files(folder,args.database_path)


    




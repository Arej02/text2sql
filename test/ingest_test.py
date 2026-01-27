import pytest
import pandas as pd
from pathlib import Path
from scripts.ingest import normalize_columns,normalize_file

# 1) normalize_file()
BASE_PATH=Path(__file__)
# Checks if it returns the stem and lowers the path
def test_normalize_file_stem():
    assert normalize_file(BASE_PATH/"DATA"/"HRC")=="hrc"

# Checks if it strips the extra spaces
def test_normalize_file_space():
    assert normalize_file(BASE_PATH/"DATA"/"  HRC.csv")=="hrc"

# 2) normalize_columns()
students=[
    [100,120,9.0],
    [98,100,8.7],
    [34,98,7.5]
]
df=pd.DataFrame(students,columns=["MArKs ","Intelligence quotient","GPA"])

def test_columns():
    df_copy=normalize_columns(df)
    assert df_copy.columns.to_list()==["marks","intelligence_quotient","gpa"]
    
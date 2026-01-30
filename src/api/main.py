from fastapi import FastAPI
from sqlalchemy import create_engine,inspect
from dotenv import load_dotenv,find_dotenv
from src.api.schemas import InputSchema,OutputSchema
from src.agent.graph import text_to_sql
import os

# Setting up the environment variables:
load_dotenv(find_dotenv())
key=os.getenv("DATABASE_URL")

if not key:
    raise ValueError("Datbase doesnot exist")
print("Successfully connected")

# Intializing the inspect object:
engine=create_engine(key)
insp=inspect(engine)

app=FastAPI()

# Home Endpoint:
@app.get("/")
def home():
    return {"message":"Welcome to Text to SQL Agent"}

# Get table names in the database:
@app.get("/tables")
def get_table_names():
    tables=insp.get_table_names()
    return {
        "table": tables
    }

# Get the feature name of each table
@app.get("/schemas")
def get_schema():
    new_dict={}
    for col in insp.get_table_names():
        new_list=[]
        for val in insp.get_columns(col):
            features=val.get("name","")
            new_list.append(features)

        new_dict[col]=new_list
    return new_dict

# Convert the natural language to SQL endpoint:
@app.post("/convert")
def convert(question:InputSchema):
    result=text_to_sql(question.question)

    return {
        "Question":question.question,
        "SQL Query":result["sql"],
        "Feedback":result["feedback"]
    }



    

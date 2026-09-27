from pydantic import BaseModel,Field
from typing import Annotated

class InputSchema(BaseModel):
    question:Annotated[str,Field(...,description="Enter your question here based on you database",example="Who got the highest marks")]
    thread_id:str="default"

class OutputSchema(BaseModel):
    Question: str
    SQL_Query: Annotated[str, Field(..., description="SQL query generated for the question")]
    Confidence_Score: Annotated[
        float,
        Field(..., description="Confidence in the generated SQL, from 0 to 1", ge=0, le=1),
    ]
    Feedback: Annotated[str, Field(..., description="Feedback about the query or question")]
    Rows_Count: int
    Rows: list[dict]
    Execution_Time_Ms: Annotated[
        float,
        Field(..., description="Database query execution time in milliseconds"),
    ]
    Messages: list[dict]

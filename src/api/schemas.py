from pydantic import BaseModel,Field
from typing import Annotated

class InputSchema(BaseModel):
    question:Annotated[str,Field(...,description="Enter your question here based on you database",example="Who got the highest marks")]
    thread_id:str="default"

class OutputSchema(BaseModel):
    question:str
    sql:Annotated[str,Field(...,description="SQL query as per the question")]
    confidence_score:Annotated[float,Field(...,description="Confidence score in a sclae of 0 to 1",ge=0,le=1)]
    feedback:Annotated[str,Field(...,description="Feedback in a line about the query or if the question was not understood")]
    rows_count:int
    rows:list[dict]
    messages:list[dict]
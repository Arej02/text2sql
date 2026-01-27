from pydantic import BaseModel,Field
from typing import TypedDict,Annotated

class StateSchema(TypedDict):
    question:str
    max_iteration:int

    sql:str
    confidence_score:float
    feedback:str

    iteration:int


class SQLSchema(BaseModel):
    sql:Annotated[str,Field(...,description="SQL query as per the question")]
    confidence_score:Annotated[float,Field(...,description="Confidence score in a sclae of 0 to 1",ge=0,le=1)]
    feedback:Annotated[str,Field(...,description="Feedback in a line about the query or if the question was not understood")]

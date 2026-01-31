from pydantic import BaseModel,Field
from typing import TypedDict,Annotated,List

class StateSchema(TypedDict):
    schema:dict[str,List[str]]
    question:str
    max_iteration:int=3
    is_answerable:bool

    sql:str
    confidence_score:float
    feedback:str

    rows:List[dict]
    iteration:int=0


class SQLSchema(BaseModel):
    sql:Annotated[str,Field(...,description="SQL query as per the question")]
    confidence_score:Annotated[float,Field(...,description="Confidence score in a sclae of 0 to 1",ge=0,le=1)]
    feedback:Annotated[str,Field(...,description="Feedback in a line about the query or if the question was not understood")]
    is_answerable:Annotated[bool,Field(...,description="true only if a valid SELECT query can be generated from the provided schema")]

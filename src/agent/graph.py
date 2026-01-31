from langchain_groq import ChatGroq
from dotenv import load_dotenv,find_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import ChatPromptTemplate
from src.agent.schemas import StateSchema,SQLSchema
from src.agent.guardrail import validate_sql
from sqlalchemy import create_engine
from src.database.schemas import schema_table
from src.database.db_connection import query_db
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import BaseMessage, add_messages
from langchain_core.messages import HumanMessage,AIMessage
from pathlib import Path
import os
import json

load_dotenv(find_dotenv())
key=os.getenv("GROQ_API_KEY")
if not key:
    raise ValueError("API Key dosnot exist")

db_key=os.getenv("DATABASE_URL")
if not db_key:
    raise ValueError("Database Key dosnot exist")

engine=create_engine(db_key)

model=ChatGroq(model="llama-3.3-70b-versatile",temperature=0)
model2=model.with_structured_output(SQLSchema)

BASE=Path(__file__).resolve().parent.parent.parent
FILE_PATH=BASE/"data"/"table_schema"

def create_sql_graph():
    with open(FILE_PATH,'w',encoding="utf-8") as f:
        data=schema_table(engine)
        json.dump(data,f,indent=2)
        

    def load_schema(state:StateSchema)->StateSchema:
        return {
            "schema":schema_table(engine)
        }

    def sql_generator(state:StateSchema)->StateSchema:
        sys_inst1="""
        You are an SQL expert. You have access to the conversation history and the current database schema. Given a schema and a natural question you will return ONLY a valid JSON object with the following keys:
        {{
        "sql":"The optimized SELECT SQL query — use empty string \"\" if the question cannot be answered with the schema",
        "confidence_score":"A float number between 0 to 1 regarding how confident you are if the query will work.",
        "feedback":"Any feedback about the query or the question",
        "is_answerable": true or false
        }}
        """
        messages=state["messages"]
        prompt=ChatPromptTemplate.from_messages([
            ("system",sys_inst1),
            *messages,
            ("human","""
            ----------Rule-----------
            1. You must only return SELECT statement
            2. Do not add any extra explanation,comments or markdowns
            3. Use only the schema that is provided.
            4. If the question:
                - is not about retrieving data from this schema
                - asks for general knowledge, math, opinions, code, jokes, etc.
                - requires information not present in the schema
                - is vague / ambiguous / off-topic
                → MUST set "is_answerable": false, "sql": "", confidence_score low (≤ 0.2), and explain clearly in feedback
             5. Never return null for sql only use "" instead
            Schema:{schema}
            Question:{user_question}""")
            ])
        
        chain=prompt | model2
        response=chain.invoke({"user_question":state["question"],"schema":state["schema"]})

        if not response.is_answerable or not response.sql.strip():
            return {
                **state,
                "sql":"",
                "confidence_score":0.0,
                "feedback":"Question cannot be answered with the schema"
            }
        
        try:
            validated_query = validate_sql(response.sql)
        except ValueError as e:
            return {
                **state,
                "sql":"",
                "confidence_score":0.0,
                "feedback":f"Invalid SQL generated: {str(e)}"
            }
        

        
        return {
            **state,
            "sql":validated_query,
            "confidence_score":response.confidence_score,
            "feedback":response.feedback,
            "messages":add_messages(state["messages"],
                                    [HumanMessage(content=state["question"]),
                                    AIMessage(content=f"Generated SQL:{validated_query}\nFeedback:{response.feedback}")])
            }
    
    def route_after_generation(state:StateSchema):
        if state["sql"]:
            return "execute_query"
        else:
            return END
        
    def execute_query(state:StateSchema)->StateSchema:
        raw_rows = query_db(state["sql"], engine)
        serializable_rows = [dict(row) for row in raw_rows]

        return {
            **state,
            "rows":serializable_rows
        }

    graph=StateGraph(StateSchema)

    graph.add_node('load_schema',load_schema)
    graph.add_node('sql_generator',sql_generator)
    graph.add_node('execute_query',execute_query)

    graph.add_edge(START,'load_schema')
    graph.add_edge('load_schema','sql_generator')
    graph.add_conditional_edges('sql_generator',route_after_generation,{"execute_query":"execute_query",END:END})
    graph.add_edge('execute_query',END)

    memory=InMemorySaver()
    workflow=graph.compile(checkpointer=memory)

    return workflow

sql_workflow=create_sql_graph()

def text_to_sql(user_question:str,thread_id:str):
    config = {"configurable": {"thread_id": thread_id}}
    initial_state={
        "question":user_question,
        "messages":[]
    }
    result=sql_workflow.invoke(initial_state,config=config)
    return {
        "sql":result["sql"],
        "confidence_score":result["confidence_score"],
        "feedback":result["feedback"],
        "rows":result.get('rows',[]),
        "messages":result.get("messages",[])
    }


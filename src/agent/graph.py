from langchain_groq import ChatGroq
from dotenv import load_dotenv,find_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import ChatPromptTemplate
import os
from src.agent.schemas import StateSchema,SQLSchema

load_dotenv(find_dotenv())
key=os.getenv("GROQ_API_KEY")
if not key:
    raise ValueError("API Key dosnot exist")

model=ChatGroq(model="llama-3.3-70b-versatile",temperature=0)
model2=model.with_structured_output(SQLSchema)

def creat_sql_graph():
    def sql_generator(state:StateSchema)->StateSchema:
        sys_inst1="""
        You are an SQL expert. Given a schema and a natural question you will return ONLY a valid JSON object with the following keys:
        {{
        "sql":"The optimized SQL query for the question",
        "confidence_score":"A float number between 0 to 1 regarding how confident you are if the query will work.",
        "feedback":"Any feedback about the query or the question"
        }}
        """

        prompt=ChatPromptTemplate.from_messages([
            ("system",sys_inst1),
            ("human","""
            ----------Rule-----------
            1. You must only return SELECT statement
            2. DO not add any extra explanation,comments or markdowns
            3. Use only the schema that is provided.
            Question:{user_question}""")
            ])
        
        chain=prompt | model2
        response=chain.invoke({"user_question":state["question"]})

        return {
            "sql":response.sql,
            "confidence_score":response.confidence_score,
            "feedback":response.feedback
        }
    graph=StateGraph(StateSchema)

    graph.add_node('sql_generator',sql_generator)

    graph.add_edge(START,'sql_generator')
    graph.add_edge('sql_generator',END)

    workflow=graph.compile()

    return workflow

sql_workflow=creat_sql_graph()

def text_to_sql(user_question):
    result=sql_workflow.invoke({"question":user_question})
    return {
        "sql":result["sql"],
        "confidence_score":result["confidence_score"],
        "feedback":result["feedback"]
    }


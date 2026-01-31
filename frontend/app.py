import streamlit as st
import requests
import pandas as pd
import uuid

st.title("Text2SQL Chat")
API_URL = "http://127.0.0.1:8000/convert"

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "chat-1"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input=st.chat_input("Ask a question about your data:")

if user_input:

    st.session_state["chat_history"].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    answer = "**Error:** Could not connect to the backend or process the response."
    rows_preview = None
    with st.spinner("Thinking..."):
        try:
            r=requests.post(API_URL,json={
                "question":user_input,
                "thread_id":str(uuid.uuid4())
            },
            timeout=25)
            r.raise_for_status()
            data=r.json()

            sql = data.get("SQL_Query", "")
            feedback = data.get("Feedback", "")
            rows_count = data.get("Rows_Count", 0)
            rows = data.get("Rows", [])

            answer = f"**SQL:**\n```sql\n{sql}\n```\n\n"
            answer += f"**Feedback:** {feedback}\n\n"
            answer += f"**Rows returned:** {rows_count}"

            if rows:
                rows_preview = rows[:10]  
            else:
                rows_preview = None
            
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

        except Exception as e:
            answer = f"**Error:** {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

    if rows_preview:
        st.subheader("Results Preview")
        st.dataframe(rows_preview)

        if rows_preview:
            df = pd.DataFrame(rows_preview)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )




                




    

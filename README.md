### Text2SQL:

**Convert natural language questions into SQL queries instantly — no SQL knowledge required.**

### Overview:

Text2SQL lets you query your data using natural language questions instead of writing SQL by hand.

You provide your data as CSV files → the system automatically loads them into a SQLite database → then you can ask questions like:

- "How many customers are from Victoria?"
- "What are the top 5 products by revenue in 2024?"
- "Show average order value per customer segment"

The system generates a safe SQL SELECT query, validates it, adds a LIMIT clause for safety, executes it, and displays the results in a clean table — all through a simple Streamlit interface.

### Why this matters:

SQL is powerful but has a steep learning curve. Many people want to explore data without learning a new language. Text2SQL removes that barrier — whether you're a business analyst, manager, student, or just curious — you can now "talk" to your database.

### Key Insights & Features

1. **Zero-configuration data loading**  
   Simply place all your `.csv` files in the `data/` folder and provide a database path (or let it use the default).  
   The system automatically converts each CSV into a table and stores it in a local SQLite database — no manual import steps required.

2. **Safe & controlled SQL generation**  
   - Only generates `SELECT` queries (blocks any modification statements)  
   - Automatically adds a `LIMIT` clause for safety  
   - Validates the query before execution

3. **Instant results with context**  
   - Shows the generated SQL query so you can learn/review it  
   - Displays the number of rows returned  
   - Shows a preview of the results in a clean table  
   - Allows downloading the full result set as CSV

4. **Persistent conversation memory**  
   Remembers previous questions and context within the same session/thread  

5. **Export & integration friendly**  
   - Download query results directly as CSV  
   - Easy to copy the generated SQL for use in other tools  
   - Can be extended to Google Sheets / Excel export in future versions

### Tools and Technologies:

1. Python: Core Language
2. Langgraph: Workflow Orchestration
3. SQLALchemy: Database Connection
4. SQLite: Lightweight local database
5. FastAPI: Backend API
6. Streamlit: Interactive Frontend

### Project Structure



### How to run this project




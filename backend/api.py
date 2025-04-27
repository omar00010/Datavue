import duckdb, os, services.db as db, services.rag as RAG, services.langchain_pipeline as langchain
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
duckdb = db.Database()

"""

    This is the main API endpoint for the backend

"""

@app.get("/api/health")
async def root():
    """ Root endpoint to check if the API is running """
    return {"message": "The API is running! \n Welcome to the DataVue API."}


@app.get("/api/list/tables")
async def list_tables():
    """ Endpoint to list all tables in the DuckDB database """
    try:
        tables = duckdb.db_connection.execute("SHOW TABLES").fetchall()
        metadata = duckdb.getMetadata()
        return {"tables": [table[0] for table in tables], "metdata":metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tables: {str(e)}")

@app.get("/api/ask")
async def fetch_answer():
    """ Endpoint to fetch an answer from the database using RAG + LangChain """
    try:        
        tables = duckdb.db_connection.execute("SHOW TABLES").fetchall()
        metadata = duckdb.getMetadata()
        question = "What is the average age of customers in the customers table?"
        relevant_tables = RAG.process_metadata_query(duckdb, question)
        
        # The relevant tables are fed to the Lanchain agent to generate the SQL query

        #answer = langchain.get_answer(query, relevant_tables)

        
        return {"relevant_tables":relevant_tables}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract answer: {str(e)}")

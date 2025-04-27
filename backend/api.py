import duckdb, os, services.db as db, services.rag as RAG, services.langchain_pipeline as langchain
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import models.State as State

app = FastAPI()
duckdb = db.Database()
langchainPipline = langchain.LangChainPipeline()

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
        question = "What is the country with the most customers"
        # Initiate the State (DTO) object
        state: State.State = {
            "question": question,
            "sql_query": None, 
            "sql_result": None,  
            "answer": None, 
            "relevant_tables": None
        }

        # Populate the State (DTO) object
        state = RAG.process_metadata_query(duckdb, state)
        print(state["relevant_tables"])
        state = langchainPipline.write_sql_query(duckdb, state)
        

        
        return {"answer": state["answer"], "sql_query": state["sql_query"], "sql_result": state["sql_result"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract answer: {str(e)}")

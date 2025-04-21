import duckdb, os, backend.db.db as db
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
duckdbDB = db.Database()

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
        tables = duckdbDB.db_connection.execute("SHOW TABLES").fetchall()
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tables: {str(e)}")

app.get("/api/ask")
async def ask_data(query: str):
    """ Endpoint to query database data. Takes in NL query and returns queried data""" 
    try:
        # This here will be retrieved from RAG. Tables metadata are combined together, embedded and a similarity search is done to figure out what data to use
        context = None
        # Here the langhchain is invoked with the relvant context and prompt in order to generate the answer
        answer = None 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query the data: {str(e)}")




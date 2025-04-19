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
    




#Depricated
@app.post("/api/upload")
async def uploadDataFile(file: UploadFile):
    """ Endpoint to upload a CSV file and load it into DuckDB """

    # Check if the uploaded file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")
    
    table_name = duckdbDB.load_csv(file, file.filename)  # Load the CSV into DuckDB

    return {"message": f"File '{file.filename}' uploaded successfully and loaded into DuckDB"}

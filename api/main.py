import duckdb, os, database
from fastapi import FastAPI, HTTPException, UploadFile


app = FastAPI()


duckdbDB = database.Database()

@app.get("/api")
async def root():
    """ Root endpoint to check if the API is running """
    return {"message": "Welcome to the DataVue API!"}


@app.post("/api/upload")
async def uploadDataFile(file: UploadFile):
    """ Endpoint to upload a CSV file and load it into DuckDB """

    # Check if the uploaded file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")
    
    table_name = duckdbDB.load_csv(file, file.filename)  # Load the CSV into DuckDB

    return {"message": f"File '{file.filename}' uploaded successfully and loaded into DuckDB"}

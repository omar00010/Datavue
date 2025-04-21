import duckdb, os
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        """Initialize the database connection"""
        database_path = os.getenv("DATABASE_PATH")  
        self.db_connection = duckdb.connect(database=database_path)    
    
    
    async def runSQLQuery(sqlQuery: str):
        """ Run the generated SQL on the database"""
        try:
            



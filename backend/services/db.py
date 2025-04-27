import duckdb, os
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        """Initialize the database connection"""
        database_path = os.getenv("DATABASE_PATH")
        self.dialect = "duckdb"
        try:
            self.db_connection = duckdb.connect(database=database_path)    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect to database: {str(e)}")
    
    
    async def runSQLQuery(self, sqlQuery: str):
        """ Run the generated SQL on the database"""
        try:
            result = self.db_connection.execute(sqlQuery)
            return result.fetchall()
        except Exception as e:
            return f"Failed to query database: {str(e)}"
    
    def getMetadata(self):
        """Get database metadata for all tables"""
        tables_metadata = []
        tables = self.db_connection.execute("SHOW TABLES").fetchall()
        try:
            for (table_name,) in tables:
                # Get column names
                columns = self.db_connection.execute(f"PRAGMA table_info('{table_name}')").fetchdf()["name"].tolist()
                
                tables_metadata.append({
                    "name": table_name,
                    "columns": columns,
                })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {str(e)}")    
        return tables_metadata
                    



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
    
    
    """Depricated for now"""
    async def load_csv(self, file: UploadFile, file_path):
        """Load a CSV file into DuckDB"""
        # Save the file to a temporary location
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Load the CSV content into DuckDB from the file path
        table_name = "current_file"
        try:
            self.db_connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto(?)", (file_path,))
        except Exception as e:
            # Log the error for debugging
            raise HTTPException(status_code=500, detail=f"Failed to load CSV into DuckDB: {str(e)}")
        finally:
            # Ensure the file exists before attempting to delete it
            if os.path.exists(file_path):
                os.remove(file_path)

        # Set the current table for querying
        self.current_table = table_name

        return True            
            


from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv()

def process_metadata_query(db, question, k=3):
    """
    Proceces the tables metadata and returns the most relevant tables based on the query.
    This is done by embedding the metadata and performing a similarity search.
    Then, a list of (k) tables with the most relvant tables is returned.
    """

    tables_metadata = db.getMetadata()

    # Convert metadata into descriptive strings
    try:
        documents = []
        for table in tables_metadata:
            table_name = table["name"]
            columns = ", ".join(table["columns"])
            content = f"Table: {table_name}\nColumns: {columns}"
            documents.append(Document(page_content=content, metadata={"table_name": table_name, "columns": table["columns"]}))

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        # Embed the metadata documents
        embeddings = OpenAIEmbeddings() 
        faiss_store = FAISS.from_documents(documents, embeddings)

        # Perform similarity search
        search_results = faiss_store.similarity_search(question, k=k)


        relevant_tables = []
        for doc in search_results:
            relevant_tables.append(doc.metadata)  
    except Exception as e:
        raise ValueError(f"Failed to process metadata question: {str(e)}")
    return relevant_tables

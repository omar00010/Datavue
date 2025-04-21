from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

def process_metadata_query(db ,query, chunk_size=500, chunk_overlap=0, k=3):
    """
    Process metadata and perform a similarity search based on the user's query

    Returns a list of tables with the most relvant tables 
    """
    search_results = []
    tables_metadata = db.getMetadata()

    # Run embeddings and similarity search

    return search_results
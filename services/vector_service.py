from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
        _chroma_client = Chroma(
            collection_name="codebase_metrics",
            embedding_function=embeddings,
            persist_directory=Config.CHROMA_DIR
        )
    return _chroma_client

def search_repository(repo_id: str, question: str, k: int = 5):
    """
    Retrieves the most semantically relevant code chunks from the requested repo.
    """
    vectorstore = get_chroma_client()
    
    # Filter by repo_id
    results = vectorstore.similarity_search(
        question, 
        k=k, 
        filter={"repo_id": repo_id}
    )
    
    return results

from services.vector_service import search_repository

def retrieval_node(state):
    """
    Queries ChromaDB to locate mathematically aligned context chunks relevant to the user query.
    """
    question = state["question"]
    repo_id = state["repo_id"]
    
    results = search_repository(repo_id, question, k=5)
    
    docs = []
    for doc in results:
        docs.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })
        
    return {"context_docs": docs}

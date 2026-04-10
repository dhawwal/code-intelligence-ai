from typing import List, Dict
from config import Config
from services.vector_service import get_chroma_client
from langchain.schema import Document

import requests
import time

def generate_and_store_embeddings(repo_id: str, symbols: List[Dict]):
    """
    Groups symbols into Documents and stores them in ChromaDB.
    Chroma uses HuggingFaceInferenceAPIEmbeddings (defined in VectorService) to generate vectors.
    """
    vectorstore = get_chroma_client()
    docs_to_insert = []
    
    for sym in symbols:
        meta = {
            "repo_id": repo_id,
            "file": sym["file"],
            "symbol": sym["name"],
            "type": sym["type"],
            "line": sym["line"]
        }
        
        # Combine contextual metadata with raw content for superior Retrieval
        content_block = f"File: {sym['file']}\nSymbol: {sym['name']}\nType: {sym['type']}\n\nCode:\n{sym['content']}"
        doc = Document(page_content=content_block, metadata=meta)
        docs_to_insert.append(doc)

    if docs_to_insert:
        vectorstore.add_documents(docs_to_insert)
        print(f"Inserted {len(docs_to_insert)} chunks into VectorStore for {repo_id}")
    else:
        print(f"No symbols found to index for {repo_id}")

from flask import Blueprint, request, jsonify
from utils.hash_utils import generate_repo_id
from services.github_service import clone_or_pull_repo
from services.parser_service import parse_repository
from services.embedding_service import generate_and_store_embeddings

repo_bp = Blueprint('repo_bp', __name__)

import threading
from flask import current_app

@repo_bp.route('/analyze', methods=['POST'])
def analyze_repo():
    """
    Ingests a GitHub repository, parses the symbols, and stores them in ChromaDB.
    """
    data = request.get_json()
    repo_url = data.get("repo_url")
    
    if not repo_url:
        return jsonify({"error": "repo_url is required"}), 400
        
    repo_id = generate_repo_id(repo_url)
    
    # Start the process in the background
    def background_task(url, rid, app):
        with app.app_context():
            try:
                # Step 2: Clone
                path = clone_or_pull_repo(url, rid)
                
                # Step 3: Parse
                symbols = parse_repository(path)
                
                # Step 4: Embed
                generate_and_store_embeddings(rid, symbols)
                
                print(f"Background task complete for {rid}")
            except Exception as e:
                import traceback
                print(f"Background task error: {e}")
                traceback.print_exc()

    # Get the actual app instance
    app = current_app._get_current_object()
    thread = threading.Thread(target=background_task, args=(repo_url, repo_id, app))
    thread.start()
        
    return jsonify({
        "message": "Analysis started in background.",
        "repo_id": repo_id
    }), 202

@repo_bp.route('/status/<repo_id>', methods=['GET'])
def get_status(repo_id):
    """
    Checks if the repository has been successfully indexed in ChromaDB.
    """
    from services.vector_service import get_chroma_client
    vectorstore = get_chroma_client()
    
    # Check if any documents exist for this repo_id
    results = vectorstore.get(where={"repo_id": repo_id}, limit=1)
    
    if len(results['ids']) > 0:
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "indexing"}), 200

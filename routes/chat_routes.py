from flask import Blueprint, request, jsonify
from agents.workflow import execute_chat_workflow

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    """
    Handles natural language queries about the indexed codebase using LangGraph execution.
    """
    data = request.get_json()
    repo_id = data.get("repo_id")
    question = data.get("question")
    
    if not repo_id or not question:
        return jsonify({"error": "repo_id and question are required"}), 400
        
    print(f"DEBUG: Received chat request for repo_id: {repo_id}, question: {question}")
    try:
        # Step 5: Master Agentic AI Workflow
        result = execute_chat_workflow(repo_id, question)
        print(f"DEBUG: Workflow result: {result}")
        
        return jsonify({
            "answer": result.get("answer"),
            "sources": result.get("sources", [])
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

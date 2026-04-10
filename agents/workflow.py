from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.planner_agent import planner_node
from agents.retrieval_agent import retrieval_node
from agents.graph_agent import graph_node
from agents.summarizer_agent import summarizer_node

def build_workflow():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planner_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("graph", graph_node)
    workflow.add_node("summarizer", summarizer_node)
    
    # Establish sequential intelligent flow
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "retrieval")
    workflow.add_edge("retrieval", "graph")
    workflow.add_edge("graph", "summarizer")
    workflow.add_edge("summarizer", END)
    
    return workflow.compile()

# Singleton for workflow compiler to optimize executions
_workflow_app = None

def execute_chat_workflow(repo_id: str, question: str):
    global _workflow_app
    if _workflow_app is None:
        _workflow_app = build_workflow()
        
    initial_state = {
        "repo_id": repo_id,
        "question": question,
        "question_type": "",
        "context_docs": [],
        "graph_context": "",
        "final_answer": ""
    }
    
    final_state = _workflow_app.invoke(initial_state)
    
    # Structure sources mapped strictly for frontend
    sources = []
    for doc in final_state.get("context_docs", []):
        sources.append({
            "file": doc["metadata"].get("file"),
            "symbol": doc["metadata"].get("symbol"),
            "line": doc["metadata"].get("line")
        })
        
    return {
        "answer": final_state["final_answer"],
        "sources": sources
    }

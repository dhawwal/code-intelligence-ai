from typing import TypedDict, Annotated, List, Dict
import operator

class AgentState(TypedDict):
    """
    State shared across LangGraph agentic workflow execution.
    """
    repo_id: str
    question: str
    question_type: str
    context_docs: List[Dict]
    graph_context: str
    final_answer: str

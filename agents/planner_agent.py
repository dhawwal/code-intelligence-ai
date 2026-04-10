from services.groq_service import get_groq_client
import json

def planner_node(state):
    """
    Determines the intent/classification of the user query.
    """
    client = get_groq_client()
    question = state["question"]
    
    prompt = f"""
    Classify the following question into one of these exact categories:
    architecture, authentication, debugging, onboarding, dependency_analysis, code_explanation, api_flow, refactoring, general.

    Respond ONLY with a JSON object format: {{"question_type": "category"}}
    
    Question: {question}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        return {"question_type": parsed.get("question_type", "general")}
    except Exception as e:
        print("Planner error:", e)
        return {"question_type": "general"}

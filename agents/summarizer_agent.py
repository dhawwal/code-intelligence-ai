from services.groq_service import get_groq_client

def summarizer_node(state):
    """
    RAG integration utilizing Groq deepseek model to fuse LLM intelligence with Vector Context.
    """
    client = get_groq_client()
    question = state["question"]
    docs = state.get("context_docs", [])
    graph_context = state.get("graph_context", "")
    
    # Format context clearly for the LLM
    context_str = "\n\n".join(
        [f"--- File: {d['metadata']['file']} | Symbol: {d['metadata']['symbol']} | Line: {d['metadata']['line']} ---\n{d['content']}" 
         for d in docs]
    )
    
    prompt = f"""
    You are an expert, senior software developer. Analyze the provided codebase context and answer the user's question accurately.
    
    USER QUESTION: {question}
    
    EXTRACTED MODULE RELATIONSHIPS:
    {graph_context}
    
    CODEBASE CONTEXT (RAG):
    {context_str}
    
    Your response should be in clean Markdown formatting. Ensure you include:
    - Direct answer and explanation.
    - Mention exactly which files and functions implement the requested behavior.
    - Possible next steps or improvement suggestions (if applicable).
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return {"final_answer": answer}
    except Exception as e:
        print("Summarizer error:", e)
        return {"final_answer": f"Error generating answer: {e}"}

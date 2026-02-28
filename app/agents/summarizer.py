from app.utils.llm import get_llm


def summarizer_node(state):
    query = state["query"]
    context = state["retrieved_context"]

    llm = get_llm()

    prompt = f"""
    You are a research analyst.

    Using ONLY the context below, generate a structured research summary.

    If information is missing, say so clearly.

    Context:
    {context}

    Question:
    {query}

    Provide a structured summary.
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "summary": response.content
    }
from app.utils.llm import get_llm


async def summarizer_node(state):
    query = state["query"]
    context = state["retrieved_context"]

    llm = get_llm()

    prompt = f"""
    You are a research analyst tasked with producing a grounded research summary.

    Your objective is to answer the research question using ONLY the information contained in the provided context.

    Strict Grounding Rules:
    - Use only facts, claims, and information explicitly present in the context.
    - Do NOT introduce external knowledge, assumptions, frameworks, or examples not stated in the context.
    - If a concept, framework, company, or technology is not explicitly mentioned in the context, do NOT include it.
    - Do not infer missing details beyond what is clearly supported.
    - If important information needed to answer the question is missing, explicitly state: "Insufficient information in the provided context."

    Instructions:
    1. Carefully analyze the provided context.
    2. Extract only relevant facts that directly help answer the question.
    3. Synthesize those facts into a clear, concise research summary.
    4. Ensure every statement can be traced back to the context.

    Context:
    {context}

    Research Question:
    {query}

    Output Requirements:
    - Produce a concise research summary.
    - Ensure the response is fully grounded in the context.
    - Avoid speculation or unsupported conclusions.
    """

    response = await llm.ainvoke(prompt)

    return {
        **state,
        "summary": response.content
    }
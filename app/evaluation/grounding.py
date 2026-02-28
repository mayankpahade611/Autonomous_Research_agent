from app.utils.llm import get_llm 

def evaluate_grounding(summary, context):
    llm = get_llm()

    prompt = f"""
    You are a great evaluater.
    Evaluate whether the following summary is fully grounded in the provided context.

    If all claims are supported by context, respond with:
    GROUNDED

    If there are unsupported claims, respond with:
    UNGROUNDED and explain briefly.

    Context:
    {context}

    Summary:
    {summary}
    """

    response = llm.invoke(prompt)

    return response.content.strip()

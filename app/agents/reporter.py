from app.utils.llm import get_llm

def report_node(state):
    summary = state["summary"]
    query = state["query"]

    llm = get_llm()

    prompt = f"""
    You are a venture research analyst.

    Convert the following research summary into a structured investment-style memo.

    Include:

    1. Executive Summary
    2. Market Landscape
    3. Key Players
    4. Competitive Insights
    5. Risks
    6. Strategic Outlook

    Research Topic:
    {query}

    Summary:
    {summary}
    """


    response = llm.invoke(prompt)

    return {
        **state,
        "final_report": response.content
    }
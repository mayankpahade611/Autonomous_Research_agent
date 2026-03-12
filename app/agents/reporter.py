from app.utils.llm import get_llm

async def report_node(state):
    summary = state["summary"]
    query = state["query"]

    llm = get_llm()

    prompt = f"""
    You are a venture capital research analyst preparing an internal investment briefing.

    Your task is to transform the provided research summary into a clear, structured investment-style memo that helps investors quickly understand the opportunity and risks.

    Guidelines:
    - Write in a concise, analytical, and professional tone.
    - Focus on insights that are relevant for investors, founders, or strategic decision-makers.
    - Highlight major trends, competitive positioning, and potential risks.
    - Do not introduce speculative information that is not supported by the summary.
    - Organize the output using clear section headings.

    Structure the memo using the following sections:

    1. Executive Summary  
    - Brief overview of the topic and the most important insights.

    2. Market Landscape  
    - Industry overview, current trends, growth drivers, and market dynamics.

    3. Key Players  
    - Major companies, startups, or organizations involved in this space.

    4. Competitive Insights  
    - Differentiation strategies, technology advantages, or positioning within the market.

    5. Risks  
    - Market, regulatory, technological, or competitive risks that could affect the opportunity.

    6. Strategic Outlook  
    - Future trajectory of the sector and potential opportunities for investment or innovation.

    Research Topic:
    {query}

    Research Summary:
    {summary}

    Output Requirements:
    - Use clear section headings.
    - Keep the memo concise but insightful.
    - Avoid bullet overload; focus on analytical clarity.
    """


    response = await llm.ainvoke(prompt)

    return {
        **state,
        "final_report": response.content
    }
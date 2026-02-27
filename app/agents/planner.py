from app.utils.llm import get_llm

def planner_node(state):
    query = state["query"]

    llm = get_llm()

    prompt = f"""

    You are a research planner.

    Break the following research question into 3-5 focused subtopics.

    Question:
    {query}

    Return ONLY a Python list of strings.
    Example:
    ["Market size", "Key players", "Risks"]
    """

    response = llm.invoke(prompt)

    try:
        plan = eval(response.content)
    except:
        plan = [response.content]

    return {
        "query": query,
        "plan": plan
    }
    
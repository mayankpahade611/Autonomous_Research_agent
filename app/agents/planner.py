from app.utils.llm import get_llm
from app.utils.logger import log_event

def planner_node(state):
    query = state["query"]

    llm = get_llm()

    prompt = f"""

    You are an expert research planner.

    Your task is to decompose the given research question into 3–5 concise, well-defined subtopics that would help systematically explore the subject.

    Guidelines:
    - Each subtopic should represent a distinct research angle.
    - Subtopics should collectively cover the major aspects of the question.
    - Keep each subtopic short (2–6 words preferred).
    - Avoid overlap or redundancy.
    - Focus on areas that would guide deeper investigation.

    Research Question:
    {query}

    Output Format:
    Return ONLY a valid Python list of strings.
    Do not include explanations, numbering, or additional text.

    Example:
    ["Market size", "Key players", "Growth drivers", "Competitive landscape", "Risks"]
    """

    response = llm.invoke(prompt)

    try:
        plan = eval(response.content)
    except:
        plan = [response.content]

    log_event(f"Planner created {len(plan)} subtopics")

    return {
        "query": query,
        "plan": plan
    }
    
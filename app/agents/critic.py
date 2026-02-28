from app.utils.llm import get_llm
from app.utils.logger import log_event

def critic_node(state):
    query = state["query"]
    summary = state["summary"]

    llm = get_llm()

    prompt = f"""
    Evaluate the following research summary.

    Check:
    1. Is it complete?
    2. Are important aspects missing?
    3. Is it grounded?

    If acceptable, respond with:
    PASS

    If insufficient, respond with:
    FAIL and explain why.

    Question:
    {query}

    Summary:
    {summary}
    """

    response = llm.invoke(prompt)
    critique = response.content.strip()
    iteration = state.get("iteration_count", 0)

    status = "PASS" if "PASS" in critique else "FAIL"

    log_event(f"Critic status: {status}")

    return {
        **state, 
        "critique": critique,
        "status": status,
        "iteration_count": iteration + 1
    }
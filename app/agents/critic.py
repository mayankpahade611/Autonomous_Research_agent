from app.utils.llm import get_llm
from app.utils.logger import log_event

def critic_node(state):
    query = state["query"]
    summary = state["summary"]

    llm = get_llm()

    prompt = f"""
    You are a research quality evaluator.

    Your task is to critically evaluate the provided research summary in relation to the original research question.

    Evaluation Criteria:
    1. Completeness — Does the summary sufficiently address the main question?
    2. Coverage — Are any major aspects, perspectives, or important details missing?
    3. Grounding — Are the claims supported by the provided information, or do they appear speculative or unsupported?

    Instructions:
    - Carefully compare the research question with the summary.
    - Identify whether the summary adequately covers the core aspects required to answer the question.
    - Detect missing critical information or logical gaps.
    - Flag any statements that appear ungrounded, exaggerated, or unsupported.

    Decision Rules:
    - If the summary is sufficiently complete, relevant, and grounded → respond with **PASS**.
    - If the summary is incomplete, missing important aspects, or contains unsupported claims → respond with **FAIL** and briefly explain the reasons.

    Research Question:
    {query}

    Research Summary:
    {summary}

    Output Format:
    Respond with ONLY one of the following formats:

    PASS

    or

    FAIL
    <brief explanation of the issues>
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
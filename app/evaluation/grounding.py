from app.utils.llm import get_llm 

def evaluate_grounding(summary, context):
    llm = get_llm()

    prompt = f"""
    You are a research grounding evaluator.

    Your task is to determine whether the provided summary is supported by the given context.

    Evaluation Instructions:
    - Carefully compare the statements in the summary with the information in the context.
    - Only use the provided context for evaluation.
    - Do NOT assume external knowledge.
    - Reasonable summarization, paraphrasing, or abstraction of the context is allowed.
    - The summary does not need to repeat the context verbatim, but its claims must remain consistent with it.

    Decision Criteria:

    GROUNDED
    - All claims in the summary are supported by the context.
    - No new facts, entities, or conclusions are introduced.

    PARTIALLY_GROUNDED
    - Most of the summary is supported by the context.
    - Some statements contain minor assumptions, interpretations, or information that cannot be directly verified from the context.
    - These additions do not significantly change the overall meaning.

    UNGROUNDED
    - The summary introduces new entities, frameworks, or concepts not present in the context.
    - The summary contains fabricated facts or unsupported claims.
    - The summary makes incorrect or contradictory statements relative to the context.

    Important:
    - Do NOT evaluate writing quality or completeness.
    - Only evaluate whether the summary is factually grounded in the context.

    Context:
    {context}

    Summary:
    {summary}

    Output Format:
    Respond with ONLY one of the following labels.

    GROUNDED
    <brief explanation of supported parts>

    or

    PARTIALLY_GROUNDED
    <brief explanation of unsupported parts>

    or

    UNGROUNDED
    <brief explanation of unsupported claims>
    """

    response = llm.invoke(prompt)

    return response.content.strip()

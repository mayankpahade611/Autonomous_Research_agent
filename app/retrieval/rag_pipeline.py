from app.retrieval.retriever import retrieve_documents
from app.utils.llm import get_llm

def generate_answer(query: str):
    docs = retrieve_documents(query)

    context = "\n\n".join([doc.page_content for doc, _ in docs])

    prompt = f"""
    You are a research assistant responsible for providing accurate, evidence-based answers.

    Your task is to answer the user's question using ONLY the information contained in the provided context.

    Strict Rules:
    - Use only facts explicitly stated in the context.
    - Do NOT introduce external knowledge, assumptions, or inferred information.
    - Do NOT fabricate details or fill gaps with speculation.
    - If the answer cannot be directly supported by the context, respond with:
    "I don't have enough information in the provided sources."

    Instructions:
    1. Carefully read and analyze the provided context.
    2. Identify the information that directly addresses the question.
    3. Provide a clear and concise answer based solely on the context.
    4. Ensure every claim in your answer can be traced back to the context.

    Context:
    {context}

    Question:
    {query}

    Output Requirements:
    - Provide a long, factual answer.
    - Do not include information that is not present in the context.
    """

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in docs]
    }
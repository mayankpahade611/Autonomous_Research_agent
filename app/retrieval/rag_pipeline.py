from app.retrieval.retriever import retriever_document
from app.utils.llm import get_llm

def generate_answer(query: str):
    docs = retriever_document(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are a research assistant.

    Answer ONLY using the provided context.
    If the answer is not explicitly present in the context, say:
    "I don't have enough information in the provided sources."

    Do NOT fabricate.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in docs]
    }
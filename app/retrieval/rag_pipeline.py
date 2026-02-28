from app.retrieval.retriever import retrieve_documents
from app.utils.llm import get_llm

def generate_answer(query: str):
    docs = retrieve_documents(query)

    context = "\n\n".join([doc.page_content for doc, _ in docs])

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
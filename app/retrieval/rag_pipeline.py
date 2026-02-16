from app.retrieval.retriever import retriever_document
from app.utils.llm import get_llm

def generate_answer(query: str):
    docs = retriever_document(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Use the following context to answer the question.
    If the answer is not in context, say you don't know.

    Context:
    {context}

    Question:
    {query}
    """

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in docs]
    }
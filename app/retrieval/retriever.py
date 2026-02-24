from app.retrieval.vector_store import get_vector_store


def retriever_document(query: str, k: int = 5):
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)

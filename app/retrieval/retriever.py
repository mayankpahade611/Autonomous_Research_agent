from app.retrieval.vector_store import get_vector_store


def retrieve_documents(query: str, k: int = 5, score_threshold: float = 0.5):
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)

    filtered = [
        (doc, score)
        for doc, score in results
        if score > score_threshold
    ]

    return filtered

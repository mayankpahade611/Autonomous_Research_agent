from langchain_community.retrievers import BM25Retriever
from app.retrieval.vector_store import get_vector_store

def hybrid_retrieve(query: str, k: int = 5):
    vector_store = get_vector_store()

    # dense search
    dense_results = vector_store.similarity_search_with_score(query, k=10)
    dense_docs = [doc for doc, _ in dense_results]

    #candidate pool
    candidate_docs = vector_store.similarity_search(query, k=30)

    bm25 = BM25Retriever.from_documents(candidate_docs)
    bm25.k = 10
    bm25_docs = bm25.invoke(query)


    # Reciprocal rank fusion
    scores = {}

    for rank, doc in enumerate(dense_docs):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1 / (rank + 60)

    for rank, doc in enumerate(bm25_docs):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1 / (rank + 60)

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse=True)

    doc_lookup = {doc.page_content: doc for doc in dense_docs + bm25_docs}

    final_docs = [doc_lookup[key] for key, _ in ranked[:k]]

    return final_docs
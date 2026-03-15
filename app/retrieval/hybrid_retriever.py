from langchain_community.retrievers import BM25Retriever
from app.retrieval.vector_store import get_vector_store
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def hybrid_retrieve(query: str, k: int = 5):
    vector_store = get_vector_store()
    loop = asyncio.get_event_loop()

    candidate_docs = await loop.run_in_executor(
        executor,
        lambda: vector_store.similarity_search_with_score(query, k=30)
    )
    all_docs = [doc for doc, _ in candidate_docs]
    dense_docs = all_docs[:10]


    bm25_docs = await loop.run_in_executor(
        executor,
        lambda: BM25Retriever.from_documents(all_docs, k=10).invoke(query)
    )


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
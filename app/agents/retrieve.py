from app.retrieval.retriever import retrieve_documents
from app.utils.logger import log_event

def retrieve_node(state):
    query = state["query"]

    results = retrieve_documents(query, k = 5)

    log_event(f"Retrieved {len(results)} documents")

    context = "\n\n".join(
        [doc.page_content for doc, _ in results]
    )

    coverage_score = min(1.0, len(results) / 5)

    return {
        **state,
        "retrieved_context": context,
        "retrieved_count": len(results),
        "coverage_score": coverage_score
    }
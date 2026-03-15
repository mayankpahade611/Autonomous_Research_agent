from app.retrieval.hybrid_retriever import hybrid_retrieve

async def retrieve_node(state):
    query = state["query"]
    docs = await hybrid_retrieve(query, k=5)
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return {
        **state,
        "retrieved_context": context,
        "retrieved_count": len(docs)
    }
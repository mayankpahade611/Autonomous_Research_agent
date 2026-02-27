from app.retrieval.ingest import ingest_document


def store_node(state):
    documents = state["documents"]

    for doc in documents:
        ingest_document(
            text=doc["content"],
            metadata={"source": doc["url"]}
        )

    return state
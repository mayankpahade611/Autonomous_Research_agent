from app.retrieval.chunking import split_text
from app.retrieval.vector_store import get_vector_store

def ingest_document(text: str, metadata: dict = None):
    vector_store = get_vector_store()
    chunks = split_text(text)


    vector_store.add_texts(
        texts=chunks,
        metadatas=[metadata or {} for _ in chunks]
    )

    return len(chunks)
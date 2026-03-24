from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from app.retrieval.embeddings import get_embedding_model
from app.config import settings
from functools import lru_cache

COLLECTION_NAME = "research_docs"

@lru_cache
def get_qdrant_client():
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )

    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    return client

@lru_cache
def get_vector_store():
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=COLLECTION_NAME,
        embedding=get_embedding_model(),  
    )
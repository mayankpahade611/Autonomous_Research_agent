from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

COLLECTION_NAME = "research_docs"


def get_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    client = QdrantClient(
        url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
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

    return Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )
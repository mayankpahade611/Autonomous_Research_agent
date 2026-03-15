from langchain_community.embeddings import HuggingFaceEmbeddings


_embeddings_model = None


def get_embedding_model():
    global _embeddings_model
    if _embeddings_model is None:
        _embeddings_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    
    return _embeddings_model

    
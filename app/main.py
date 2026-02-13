from fastapi import FastAPI
from app.retrieval.vector_store import get_vector_store

app = FastAPI(title="Autonomos Reserach Agent")

@app.get("/")
def root():
    return {"message": "Research Agent running"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/test-vector")
def test_vector():
    store = get_vector_store()
    store.add_texts(["AI startups are growing rapidly in 2026."])
    return {"status": "vector saved"} 
from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval.vector_store import get_vector_store
from app.retrieval.ingest import ingest_document
from app.retrieval.rag_pipeline import generate_answer

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

class IngestRequest(BaseModel):
    text: str
    source: str = "manual_input"  # default

@app.post("/ingest")
def ingest(request: IngestRequest):
    count = ingest_document(
        text=request.text,
        metadata={"source": request.source}
    )
    return {"chunks_added": count}

@app.post("/query")
def query(question: str):
    return generate_answer(question)
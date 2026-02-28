from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval.vector_store import get_vector_store
from app.retrieval.ingest import ingest_document
from app.retrieval.rag_pipeline import generate_answer
from app.graph import research_graph
from pydantic import BaseModel
from app.evaluation.grounding import evaluate_grounding
import time


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
    source: str = "manual_input"  

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


class ResearchRequest(BaseModel):
    query: str

@app.post("/research-plan")
def generate_plan(request: ResearchRequest):
    start_time = time.time()

    result = research_graph.invoke({
        "query": request.query,
        "iteration_count": 0
    })

    grounding_status = evaluate_grounding(
        result["summary"],
        result["retrieved_context"]
    )

    end_time = time.time()

    execution_time = round(end_time - start_time, 2)

    return {
        "final_report": result["final_report"],
        "iterations": result["iteration_count"],
        "retrieved_chunks": result.get("retrieved_count", 0),
        "execution_time_seconds": execution_time,
        "grounding_check": grounding_status
    }


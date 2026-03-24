from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Autonomous Research Agent")

@app.get("/")
def root():
    return {"message": "Research Agent running"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/test-vector")
def test_vector():
    from app.retrieval.vector_store import get_vector_store
    store = get_vector_store()
    store.add_texts(["AI startups are growing rapidly in 2026."])
    return {"status": "vector saved"}

class IngestRequest(BaseModel):
    text: str
    source: str = "manual_input"

@app.post("/ingest")
def ingest(request: IngestRequest):
    from app.retrieval.ingest import ingest_document
    count = ingest_document(
        text=request.text,
        metadata={"source": request.source}
    )
    return {"chunks_added": count}

@app.post("/query")
def query(question: str):
    from app.retrieval.rag_pipeline import generate_answer
    return generate_answer(question)

class ResearchRequest(BaseModel):
    query: str

@app.post("/research-plan")
async def generate_plan(request: ResearchRequest):
    from app.graph import get_research_graph
    from app.evaluation.grounding import evaluate_grounding

    graph = get_research_graph()
    start_time = time.time()

    result = await graph.ainvoke({
        "query": request.query,
        "iteration_count": 0
    })

    grounding_status = evaluate_grounding(
        result["summary"],
        result["retrieved_context"]
    )

    return {
        "final_report": result.get("final_report"),
        "iterations": result.get("iteration_count"),
        "retrieved_chunks": result.get("retrieved_count", 0),
        "execution_time_seconds": round(time.time() - start_time, 2),
        "grounding_check": grounding_status.split("\n")[0]
    }
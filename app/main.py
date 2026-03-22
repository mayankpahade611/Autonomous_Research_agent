from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time
import uuid
import json
import redis
import os

app = FastAPI(title="Autonomous Research Agent")

# Redis client
r = redis.from_url(os.getenv("REDIS_URL"))

def save_task(task_id: str, data: dict):
    r.setex(task_id, 3600, json.dumps(data))  # saved for 1 hour ✅

def get_task(task_id: str):
    data = r.get(task_id)
    return json.loads(data) if data else None

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
async def generate_plan(request: ResearchRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    save_task(task_id, {"status": "running", "result": None, "error": None})
    background_tasks.add_task(run_research_task, task_id, request.query)
    return {"task_id": task_id, "status": "running"}

async def run_research_task(task_id: str, query: str):
    try:
        from app.graph import get_research_graph
        from app.evaluation.grounding import evaluate_grounding

        graph = get_research_graph()
        start_time = time.time()

        result = await graph.ainvoke({
            "query": query,
            "iteration_count": 0
        })

        grounding_status = evaluate_grounding(
            result["summary"],
            result["retrieved_context"]
        )

        execution_time = round(time.time() - start_time, 2)

        save_task(task_id, {
            "status": "done",
            "result": {
                "final_report": result.get("final_report"),
                "iterations": result.get("iteration_count"),
                "retrieved_chunks": result.get("retrieved_count", 0),
                "execution_time_seconds": execution_time,
                "grounding_check": grounding_status.split("\n")[0]
            },
            "error": None
        })

    except Exception as e:
        save_task(task_id, {"status": "error", "result": None, "error": str(e)})

@app.get("/research-plan/status/{task_id}")
def get_status(task_id: str):
    task = get_task(task_id)
    if not task:
        return {"status": "not_found"}
    return task
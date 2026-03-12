# from fastapi import FastAPI
# from pydantic import BaseModel
# import time

# app = FastAPI(title="Autonomos Reserach Agent")

# @app.get("/")
# def root():
#     return {"message": "Research Agent running"}

# @app.get("/health")
# def health():
#     return {"status": "OK"}

# @app.get("/test-vector")
# def test_vector():
#     from app.retrieval.vector_store import get_vector_store
#     store = get_vector_store()
#     store.add_texts(["AI startups are growing rapidly in 2026."])
#     return {"status": "vector saved"} 

# class IngestRequest(BaseModel):
#     text: str
#     source: str = "manual_input"  

# @app.post("/ingest")
# def ingest(request: IngestRequest):
#     from app.retrieval.ingest import ingest_document
#     count = ingest_document(
#         text=request.text,
#         metadata={"source": request.source}
#     )
#     return {"chunks_added": count}

# @app.post("/query")
# def query(question: str):
#     from app.retrieval.rag_pipeline import generate_answer
#     return generate_answer(question)


# class ResearchRequest(BaseModel):
#     query: str

# @app.post("/research-plan")
# async def generate_plan(request: ResearchRequest):
#     from app.graph import get_research_graph
#     from app.evaluation.grounding import evaluate_grounding
#     graph =get_research_graph()

#     start_time = time.time()

#     result = await graph.ainvoke({
#         "query": request.query,
#         "iteration_count": 0
#     })

#     grounding_status = evaluate_grounding(
#         result["summary"],
#         result["retrieved_context"]
#     )

#     end_time = time.time()

#     execution_time = round(end_time - start_time, 2)

#     return {
#         "final_report": result.get("final_report"),
#         "iterations": result.get("iteration_count"),
#         "retrieved_chunks": result.get("retrieved_count", 0),
#         "execution_time_seconds": execution_time,
#         "grounding_check": grounding_status
#     }

# from fastapi import FastAPI

# app = FastAPI(title="Autonomous Research Agent")

# @app.get("/")
# def root():
#     return {"message": "Research Agent running"}

# @app.get("/health")
# def health():
#     return {"status": "OK"}

# @app.post("/research-plan")
# async def generate_plan(request: ResearchRequest):
#     try:
#         from app.graph import get_research_graph
#         graph = get_research_graph()

#         result = await graph.ainvoke({
#             "query": request.query,
#             "iteration_count": 0
#         })

#         return result

#     except Exception as e:
#         return {"error": str(e)}


from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time
import uuid

app = FastAPI(title="Autonomous Research Agent")

# In-memory task store (fine for single worker on Render)
task_store = {}

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
    count = ingest_document(text=request.text, metadata={"source": request.source})
    return {"chunks_added": count}

@app.post("/query")
def query(question: str):
    from app.retrieval.rag_pipeline import generate_answer
    return generate_answer(question)

class ResearchRequest(BaseModel):
    query: str

# ✅ Step 1: Start the research — returns instantly
@app.post("/research-plan")
async def generate_plan(request: ResearchRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_store[task_id] = {"status": "running", "result": None, "error": None}
    background_tasks.add_task(run_research_task, task_id, request.query)
    return {"task_id": task_id, "status": "running"}  # returns in <1s ✅

# ✅ Step 2: The actual heavy work runs in background
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

        task_store[task_id] = {
            "status": "done",
            "result": {
                "final_report": result.get("final_report"),
                "iterations": result.get("iteration_count"),
                "retrieved_chunks": result.get("retrieved_count", 0),
                "execution_time_seconds": execution_time,
                "grounding_check": grounding_status
            },
            "error": None
        }

    except Exception as e:
        task_store[task_id] = {"status": "error", "result": None, "error": str(e)}

# ✅ Step 3: Poll this until status = "done"
@app.get("/research-plan/status/{task_id}")
def get_research_status(task_id: str):
    task = task_store.get(task_id)
    if not task:
        return {"status": "not_found"}
    return task
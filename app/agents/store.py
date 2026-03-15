import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.retrieval.ingest import ingest_document

executor = ThreadPoolExecutor()

async def store_node(state):
    documents = state["documents"]
    loop = asyncio.get_event_loop()

    async def ingest_one(doc):
        await loop.run_in_executor(
            executor,
            ingest_document,
            doc["content"],
            {"source": doc["url"]}
            )
    
    
    await asyncio.gather(*[ingest_one(doc) for doc in documents])
    return state
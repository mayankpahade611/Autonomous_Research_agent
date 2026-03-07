from tavily import TavilyClient
from app.config import settings
import asyncio


client = TavilyClient(api_key = settings.TAVILY_API_KEY)

async def search_subtopic(query, subtopic):
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: client.search(
            query=f"{query} - {subtopic}",
            search_depth="advanced",
            max_results=3
        )
    )

    return response["results"]


async def parallel_search(query, plan):
    tasks = [
        search_subtopic(query, subtopic)
        for subtopic in plan 
    ]

    results = await asyncio.gather(*tasks)

    flattened = []
    for r in results:
        flattened.extend(r)

    return flattened


async def search_node(state):
    query = state["query"]
    plan = state["plan"]

    result = await parallel_search(query, plan)

    return {
        **state,
        "search_results": result
    }
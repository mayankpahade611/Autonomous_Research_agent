from tavily import TavilyClient
from app.config import settings


def search_node(state):
    query = state["query"]
    plan = state["plan"]

    client = TavilyClient(api_key = settings.TAVILY_API_KEY)

    all_results = []

    for subtopics in plan:
        response = client.search(
            query=f"{query} - {subtopics}",
            search_depth="advanced",
            max_results=3
        )

        for result in response["results"]:
            all_results.append({
                "title": result["title"],
                "url": result["url"],
                "content": result["content"]
            })

        return {
            "query":query,
            "plan": plan,
            "search_results": all_results
        }
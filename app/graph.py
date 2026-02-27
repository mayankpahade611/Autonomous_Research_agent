from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph,START, END
from app.agents.planner import planner_node
from app.agents.search import search_node
from app.agents.scraper import scrape_node
from app.agents.store import store_node

class ResearchState(TypedDict):
    query: str
    plan: List[str]
    search_results: List[Dict]
    documents: List[Dict]

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("scraper", scrape_node)
workflow.add_node("store", store_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "search")
workflow.add_edge("search", "scraper")
workflow.add_edge("scraper", "store")
workflow.add_edge("store", END)

research_graph = workflow.compile()

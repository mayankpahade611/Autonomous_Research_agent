from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph,START, END
from app.agents.planner import planner_node
from app.agents.search import search_node
from app.agents.scraper import scrape_node
from app.agents.store import store_node
from app.agents.retrieve import retrieve_node
from app.agents.summarizer import summarizer_node
from app.agents.critic import critic_node
from app.agents.reporter import report_node   


class ResearchState(TypedDict):
    query: str
    plan: List[str]
    search_results: List[Dict]
    documents: List[Dict]
    retrieved_context: str
    retrieved_count: int
    summary: str
    critique: str
    status: str
    iteration_count: int
    final_report: str

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("scraper", scrape_node)
workflow.add_node("store", store_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("critic", critic_node)
workflow.add_node("report", report_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "search")
workflow.add_edge("search", "scraper")
workflow.add_edge("scraper", "store")
workflow.add_edge("store", "retrieve")
workflow.add_edge("retrieve", "summarizer")
workflow.add_edge("summarizer", "critic")
workflow.add_edge("critic", "report")


research_graph = workflow.compile()

def route_after_critic(state):
    if state["status"] == "PASS":
        return "report"
    
    if state["iteration_count"] >= 2:
        return "report"
    
    return "retrieve"

workflow.add_conditional_edges(
    "critic",
    route_after_critic
)

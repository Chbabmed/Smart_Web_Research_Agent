from langgraph.graph import StateGraph, END
from nodes import planner, scraper, evaluator, summarizer
from state import ResearchState

def should_continue(state: ResearchState) -> str:
    """
    Conditional edge from evaluator:
    - If sufficient → summarize
    - If not → go back to planner for more URLs
    """
    if state.get("is_sufficient"):
        return "summarize"
    return "replan"

def build_graph():
    graph = StateGraph(ResearchState)

    # add nodes
    graph.add_node("planner", planner.planner_node)
    graph.add_node("scraper", scraper.scraper_node)
    graph.add_node("evaluator", evaluator.evaluator_node)
    graph.add_node("summarizer", summarizer.summarizer_node)

    # entry point
    graph.set_entry_point("planner")

    # add edges
    graph.add_edge("planner", "scraper")
    graph.add_edge("scraper", "evaluator")

    graph.add_conditional_edges(
        "evaluator",
        should_continue,
        {"summarize": "summarizer", "replan": "planner"}

    )

    graph.add_edge("summarizer", END)

    return graph.compile()

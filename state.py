from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    question: str
    urls_to_scrape: list[str]
    scraped_pages: Annotated[list[str], operator.add]
    is_sufficient: bool # LLM verdict : is data sufficient to answer the question?
    loop_count: int # of times the research loop has been executed
    final_report: str
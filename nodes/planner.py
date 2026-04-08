from http.client import responses

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from state import ResearchState

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

def planner_node(state: ResearchState) -> dict:
    """
    Takes the research question and decide which URLs to scrape.
    On subsequent loops, it tries to find different/better sources
    """
    print("[Planner] Planning which URLs to scrape...")

    loop = state.get("loop_count", 0)
    already_scraped = [p["url"] for p in state.get("scraped_pages", [])]

    system_prompt = """You are a research planner. Given a research question, 
your job is to return a list of 3-4 real, publicly accessible URLs that would 
contain useful information to answer the question.
 
Rules:
- Return ONLY a plain list of URLs, one per line. No numbering, no explanation.
- Prefer documentation sites, reputable blogs, GitHub repos, or comparison articles.
- Do NOT include paywalled sites like Medium members-only or NYT.
- Do NOT repeat URLs already scraped.
"""
    already_str = (
        f"\nAlready scraped (do not repeat):\n" + "\n".join(already_scraped)
        if already_scraped else ""
    )

    loop_hint = (
        f"\nThis is retry #{loop}. Try different or more specific sources."
        if loop > 0 else ""
    )

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Research question: {state['question']}{already_str}{loop_hint}")
        ]
    )

    raw = response.content.strip() # expecting a list of URLs, one per line
    urls = [line.strip() for line in raw.splitlines() if line.strip().startswith("http")] # basic validation to filter out non-URLs

    print(f" -> Found {len(urls)} URLs to scrape.")
    for url in urls:
        print(f"    - {url}")

    return {
        "urls_to_scrape": urls,
        "loop_count": loop + 1
    }




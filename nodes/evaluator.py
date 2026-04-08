from http.client import responses

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import ResearchState

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

MAX_LOOP = 3

def evaluator_node(state: ResearchState) -> dict:
    """
    Reads all scraped content and decides if there's enough information
    to answer the research question. Returns is_sufficient = True/False.
    """

    print("\n🔍 [Evaluator] Checking if gathered data is sufficient...")

    loop_count = state.get("loop_count", 1)

    if loop_count >= MAX_LOOP:
        print(f" -> Reached max loop count ({MAX_LOOP}). Marking as sufficient to prevent infinite loops.")
        return {"is_sufficient": True}

    scraped = state.get("scraped_pages", [])
    usefull_pages = [p for p in scraped if p.get("content")]

    if not usefull_pages:
        print(" -> No useful content found in scraped pages.")
        return {"is_sufficient": False}

    content_summary = ""

    for page in usefull_pages:
        content_summary += f"URL: {page['url']}\nContent:\n{page['content'][:800]}\n\n"

    system_prompt = """You are a research evaluator. Given a question and some scraped web content,
decide if there is ENOUGH information to write a comprehensive answer.

Reply with ONLY one word: YES or NO.
- YES = the content clearly covers the topic with enough detail to answer well
- NO = the content is too thin, off-topic, or missing key aspects
"""
    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=(
                f"Question: {state['question']}\n\n"
                f"Scraped content so far:\n{content_summary}"
            ))        ]
    )

    verdict = response.content.strip().upper()
    is_sufficient = verdict.startswith("YES")

    print(f"  → Verdict: {'✅ Sufficient' if is_sufficient else '🔄 Need more data'}")

    return {"is_sufficient": is_sufficient}
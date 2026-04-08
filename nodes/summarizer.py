from http.client import responses

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import ResearchState

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

def summarizer_node(state: ResearchState)-> dict :
    """
    Synthesizes all scraped content into a clean, structured final report.
    """
    print("\n✍️  [Summarizer] Writing final research report...")

    scraped_pages = state.get("scraped_pages", [])
    useful_pages = state.get("useful_pages", [])

    content_block = ""
    for page in useful_pages:
        content_block += f"\n-- Source: {page['url']} --\n{page['content']}\n"

    system_prompt = """You are a research analyst. Using the scraped web content provided,
write a clear, well-structured answer to the research question.

Format your report as:
## Summary
(2-3 sentence overview)

## Key Findings
(bullet points of the most important insights)

## Details
(deeper explanation organized by subtopic)

## Sources
(list the URLs used)

Be factual, concise, and cite sources where relevant.
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=(
            f"Research question: {state['question']}\n\n"
            f"Scraped content:\n{content_block}"
        ))
    ])

    report = response.content.strip()
    print("  ✅ Report generated!")

    return {"final_report": report}
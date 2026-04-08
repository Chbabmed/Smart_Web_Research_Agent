from dotenv import load_dotenv
from graph import build_graph

load_dotenv()


def run_research(question: str):
    print("\n" + "=" * 60)
    print(f"🔬 Research Question: {question}")
    print("=" * 60)

    app = build_graph()

    initial_state = {
        "question": question,
        "urls_to_scrape": [],
        "scraped_pages": [],
        "is_sufficient": False,
        "loop_count": 0,
        "final_report": "",
    }

    final_state = app.invoke(initial_state)

    print("\n" + "=" * 60)
    print("📄 FINAL REPORT")
    print("=" * 60)
    print(final_state["final_report"])
    print("\n" + "=" * 60)
    print(f"📊 Stats: {final_state['loop_count']} planning loop(s), "
          f"{len(final_state['scraped_pages'])} pages scraped")

    return final_state["final_report"]


if __name__ == "__main__":
    question = "What are the pros and cons of the top 3 Python web scraping libraries?"
    run_research(question)
from state import ResearchState
from tools.playwright_scraper import  scrape_urls_sync

def scraper_node(state: ResearchState) -> dict:
    """
    Scrapes the URLs provided by the planner node and returns the content using playwright.
    Append results to scraped_pages (operator.add handles this) and return the updated state.
    """

    urls = state.get("urls_to_scrape", [])
    print(f"\n Scraper node: Scraping {len(urls)} URLs...")

    if not urls:
        print("No URLs to scrape.")
        return {"scraped_pages": []}

    scraped_results = scrape_urls_sync(urls)

    successful = [r for r in scraped_results if r["error"] is None]
    failed = [r for r in scraped_results if r["error"]]

    print(f" -> Successfully scraped {len(successful)} pages.")

    return {"scraped_pages": scraped_results}

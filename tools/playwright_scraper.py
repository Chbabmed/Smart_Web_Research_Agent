import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def scrape_url(url: str) -> dict:
    """
    Uses Playwright to visit a URL and extract clean text content.
    Returns a dict with the url and extracted content.
    """

    print(f"> Scraping {url}...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            #Set realistic user agent to avoid bot detection
            await page.set_extra_http_headers({
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            })
            await page.goto(url, timeout=15000)

            await asyncio.sleep(2)

            html = await page.content()

            await browser.close()

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup (["script", "style", "header", "footer", "nav", "aside", "form", "input", "button", "noscript", "iframe", "svg", "canvas", "video", "audio", "picture", "source", "link", "meta", "head", "object", "embed"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        content = text[:3000] # Limit to first 3000 chars

        return {"url": url, "content": content, "error": None}
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {"url": url, "content": None, "error": str(e)}


def scrape_urls_sync(urls: list[str]) -> list[dict]:
    """
    Scrapes multiple URLs concurrently using asyncio and Playwright.
    Returns a list of dicts with url, content, and error (if any).
    """
    return asyncio.run(_scrape_all(urls))

async def _scrape_all(urls: list[str]) -> list[dict]:
    """Scrape all URLs concurrently."""
    tasks = [scrape_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def fetch_page(session, url):
    try:
        async with session.get(
            url, 
            timeout=aiohttp.ClientTimeout(total=3),  # 10s → 5s
            headers={"User-Agent": "Mozilla/5.0"}    # avoid blocks
        ) as response:
            if response.status != 200:
                return None 
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=" ")
            return {"url": url, "content": text[:2000]}  # 8000 → 3000
    except Exception:
        return None

async def scrape_url(urls):
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_page(session, url)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

    return [r for r in results if r]

async def scrape_node(state):
    
    urls = [r["url"] for r in state["search_results"]]

    documents = await scrape_url(urls)

    return {
        **state,
        "documents": documents
    }

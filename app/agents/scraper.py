import requests
from bs4 import BeautifulSoup


def scrape_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ")
        return text.strip()
    except Exception:
        return None
    

def scrape_node(state):
    search_results = state["search_results"]

    documents = []

    for result in search_results:
        url = result["url"]
        content = scrape_url(url)

        if content and len(content) > 500:
            documents.append({
                "url": url,
                "content": content
            })

    return {
        **state,
        "documents": documents
    }

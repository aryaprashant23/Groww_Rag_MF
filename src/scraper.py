import os
import urllib.request
from bs4 import BeautifulSoup

URLS = [
    "https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/nippon-india-multi-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/nippon-india-silver-etf-fof-direct-growth"
]

def fetch_and_clean_html(url: str) -> str:
    """Fetches HTML from a URL and extracts pure factual text."""
    print(f"Fetching: {url}")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove non-content elements like nav, footer, script, styles, etc.
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "button", "iframe"]):
        element.decompose()
        
    # Get text
    text = soup.get_text(separator=' ')
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def scrape_all():
    docs = []
    for url in URLS:
        text = fetch_and_clean_html(url)
        if text:
            docs.append({"url": url, "text": text})
            print(f"Successfully extracted {len(text)} characters from {url}")
    return docs

if __name__ == "__main__":
    docs = scrape_all()
    # Save extracted texts for debugging and manual verification
    os.makedirs("data", exist_ok=True)
    for i, doc in enumerate(docs):
        # Extract the fund slug from URL for the filename
        filename = doc["url"].split("/")[-1]
        filepath = os.path.join("data", f"{filename}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {doc['url']}\n\n")
            f.write(doc["text"])
    print("Scraping complete. Extracted text saved in the 'data' directory.")

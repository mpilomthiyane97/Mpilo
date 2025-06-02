# news_tool.py
import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool

def fetch_news() -> str:
    """Scrape top 3 latest tech headlines with links."""
    try:
        response = requests.get("https://techcrunch.com")
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select("a.post-block__title__link", limit=3)
        headlines = []
        for i, article in enumerate(articles):
            title = article.get_text(strip=True)
            link = article['href']
            headlines.append(f"{i+1}. {title} → {link}")
        return "\n".join(headlines)
    except Exception as e:
        return f"Error fetching news: {e}"

# Wrap fetch_news in a Tool object, ignoring the input string
get_news = Tool(
    name="get_news",
    func=lambda x: fetch_news(),
    description="Scrape top 3 latest tech headlines with links."
)

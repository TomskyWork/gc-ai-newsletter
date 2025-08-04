import json
import asyncio

from .scrape_substack import get_substack_articles


def scrape_url(url: str):
    """
    Scrape URLs for the specific blog / newsletter
    Returns Bool
    """

    if url is not None:
        article_list = asyncio.run(get_substack_articles(url))
        # print(f"Extracted {len(article_list)} articles")

        # cleanup json result from non titled articles
        articles = [article for article in article_list if article['article_link']!='#']

        # print(json.dumps(articles, indent=2) if articles else "No data found")
        return articles

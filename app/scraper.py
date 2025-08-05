import json
import asyncio

from scrape_substack import get_substack_articles, scrape_relevant_articles


def scrape_url(url: str):
    """
    Scrape URLs for the specific blog / newsletter
    Returns Bool
    """

    if url is not None:
        article_list = asyncio.run(get_substack_articles(url))
        print(f"Extracted {len(article_list)} articles")

        #
        # HERE  you can FILTER the list of articles from the "topics" page for example only certain dates or specific topics...
        #

        articles = [article for article in article_list if article['article_link']!='#']
        print(json.dumps(articles, indent=2) if articles else "No data found")

        #
        # SCRAPING all the pages from the list of articles above
        #
        links = [article['article_link'] for article in articles if article['article_link']!='#']
        print(json.dumps(links, indent=2) if links else "No data found")
        summary= asyncio.run(scrape_relevant_articles(links))


        return summary



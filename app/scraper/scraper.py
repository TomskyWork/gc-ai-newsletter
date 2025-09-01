import json
import asyncio
from typing import List, Annotated

from models.schemas import UrlScrapeSchema, SchemaEnum
from settings import Settings
from .pragmatic_programmer.scrape import get_pragmatic_programmer_articles
from .pragmatic_programmer.scrape_old import get_substack_articles, scrape_relevant_articles

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
        #links = [article['article_link'] for article in articles if article['article_link']!='#']
        #print(json.dumps(links, indent=2) if links else "No data found")
        summary= asyncio.run(scrape_relevant_articles(articles))


        return summary

def scrape_all_articles(urls: List[UrlScrapeSchema]):
    """
    Scrape URLs for the specific blog / newsletter
    Returns Bool
    """

    # TODO steps ?
    # receive the list of url dictionaries
    # sort them in to lists of the same schemas ?
    # run each schema through its separate scraper
    # check for existing title n date save results in DB ?
    # create timestamp of scrape time
    # get todays date and check for last 7 -14 days of article being written
    # get data from DB and do summary on those
    #------------------------------------------------
    # maybe in ai_summary it can contain multiple prompts and responses ? for comparison..
    # create endpoint that can review the article n summary n run different prompt and add those to ai_summary fields

    if urls is not None:
        for item in urls:
            match item.scrapeSchema:
                case SchemaEnum.pragmatic_programmer_blog_schema:
                    # TODO order of execution
                    # - get list of URLS, if page has multiple links to articles, get there links n names n dates if available
                    # - check in DB
                    # - scrape all articles that dont exist in DB
                    # - save in DB
                    articles = get_pragmatic_programmer_articles(item.url)
                    #TODO write to DB
                    return articles
                case SchemaEnum.unspecified_schema:
                    pass
                case _:
                    pass





    pass



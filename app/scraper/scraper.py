from typing import List

from models.schemas import UrlScrapeSchema, SchemaEnum
from .pragmatic_programmer.scrape import get_pragmatic_programmer_articles
from .troy_hunt_blog.scrape import get_troy_hunt_articles


def scrape_all_articles(urls: List[UrlScrapeSchema]):
    """
    Scrape URLs for the specific blog / newsletter
    Returns Bool
    """

    # TODO steps ?
    # receive the list of url dictionaries
    # sort them in to lists of the same schemas ?
    # run each scraper with specific page config schema
    # check for existing title n date save results in DB ?
    # get todays date and check for last 7 -14 days of article being written
    # get data from DB and do summary on those
    #------------------------------------------------
    # maybe in ai_summary it can contain multiple prompts and responses ? for comparison..
    # create endpoint that can review the article n summary n run different prompt and add those to ai_summary fields

    if urls is not None:
        for item in urls:
            match item.scrapeSchema:
                case SchemaEnum.pragmatic_programmer_blog_schema:
                    articles = get_pragmatic_programmer_articles(item.url)
                    return articles
                case SchemaEnum.troy_hunt_blog_schema:
                    articles = get_troy_hunt_articles(item.url)
                    return articles
                case SchemaEnum.unspecified_schema:
                    pass
                case _:
                    pass





    pass




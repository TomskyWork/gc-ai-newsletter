from typing import List
import datetime

from .crawler_settings import article_list_crawler_config, article_content_crawler_config
from ..crawler import crawl

async def get_pragmatic_programmer_articles(url:str):
    list_of_articles = await get_article_list(url)
    # clear empty links
    articles = [article for article in list_of_articles if article['article_link'] != '#']
    result = await get_content_from_articles(articles)
    return result

async def get_article_list(url:str):
    result = await crawl(url, article_list_crawler_config)
    return result

async def get_content_from_articles(articles: List):
    for item in articles:
        page_content = await crawl(item["article_link"], article_content_crawler_config, page_content = True)
        item['page'] = page_content
        item['ai_summary'] = ''
        item['date_scraped'] = str(datetime.date.today())
        item['tags']= []
    return articles
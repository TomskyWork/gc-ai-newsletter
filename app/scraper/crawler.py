import json
from crawl4ai import AsyncWebCrawler

from scraper.pragmatic_programmer.crawler_settings import browser_config

async def crawl(page_url, crawler_config, page_content=False):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=page_url,
            config=crawler_config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return result.error_message

        res = result.markdown if page_content else json.loads(result.extracted_content)
    return res
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy

from .article import substack_article_list_schema


async def get_substack_articles(page_url:str):

    browser_config = BrowserConfig(verbose=True)

    extraction_strategy = JsonCssExtractionStrategy(substack_article_list_schema, verbose=True)

    scraper_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,
        excluded_tags=['div.main-menu', 'div.footer'],
       # target_elements=['div.portable-archive-list'],
        exclude_external_links=True,

        # Content processing
        process_iframes=False,
        remove_overlay_elements=True,

        # CSS selection or entire page
        css_selector="div.portable-archive-list",

        # extraction config
        extraction_strategy=extraction_strategy,

        # Cache control
        cache_mode=CacheMode.DISABLED  # Use cache if available
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        # 4. Run the crawl and extraction
        result = await crawler.arun(
            url=page_url,

            config=scraper_config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return

        # 5. Parse the extracted JSON
        data = json.loads(result.extracted_content)
        return data
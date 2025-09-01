from crawl4ai import JsonCssExtractionStrategy, DefaultMarkdownGenerator, PruningContentFilter
from crawl4ai.async_configs import CrawlerRunConfig, CacheMode, BrowserConfig

from models.article import pragmatic_programmer_article_list_schema

browser_config = BrowserConfig(verbose=True)

extraction_strategy = JsonCssExtractionStrategy(pragmatic_programmer_article_list_schema, verbose=True)

article_list_crawler_config = CrawlerRunConfig(
    # Content filtering
    word_count_threshold=10,
    excluded_tags=['div.main-menu', 'div.footer'],
    exclude_external_links=True,

    # Content processing
    process_iframes=False,
    remove_overlay_elements=True,
    check_robots_txt=True,

    css_selector="div.portable-archive-list",

    # extraction config
    extraction_strategy=extraction_strategy,

    # Cache control
    cache_mode=CacheMode.DISABLED
)

article_content_crawler_config = CrawlerRunConfig(
    # Content filtering
    excluded_tags=['div.main-menu', 'div.paywall', 'div.footer','div.post-ufi'],
    target_elements=['div.available-content', 'div.single-post'],
    exclude_external_links=True,

    # Content processing
    process_iframes=False,
    remove_overlay_elements=True,
    check_robots_txt=True,

    cache_mode=CacheMode.BYPASS,

    # Streaming when scrapping in parallel
    stream=False,

    markdown_generator=DefaultMarkdownGenerator(
        # removes boilerplate
        content_filter=PruningContentFilter() ,
        options={
            "ignore_links": True,
            "skip_internal_links": True,
            "ignore_images": True,
            # Turn HTML entities into text (default is often True).
            "escape_html": True,
            #"body_width": 100
        }
    )
)

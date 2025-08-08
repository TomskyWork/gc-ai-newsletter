import json
from dotenv import load_dotenv
import os
from typing import List
from crawl4ai import AsyncWebCrawler, PruningContentFilter
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from crawl4ai import JsonCssExtractionStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_aws import ChatBedrock, BedrockLLM

from article import substack_article_list_schema

load_dotenv()
USE_OLLAMA = os.getenv("USE_OLLAMA")
USE_AWS_BEDROCK = os.getenv("USE_AWS_BEDROCK")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

if USE_OLLAMA:
    model = ChatOllama(
        model=OLLAMA_LLM_MODEL,
        temperature=0,
        reasoning= False,
    )

if not USE_OLLAMA and not USE_AWS_BEDROCK:
    model = ChatGoogleGenerativeAI(
        model=GOOGLE_LLM_MODEL,
        temperature=0,
        max_tokens=None,
        timeout=30,
        max_retries=2,
    )
if not USE_OLLAMA and USE_AWS_BEDROCK:
     model = ChatBedrock(
        model="anthropic.claude-v2",
        #provider="<ARN>",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        #beta_use_converse_api=True,
        temperature=0,
        max_tokens=None,
    )







async def get_substack_articles(page_url:str):

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


async def scrape_relevant_articles(articles: List):
    browser_config = BrowserConfig(verbose=True)

    run_config = CrawlerRunConfig(
        # Content filtering
        # excluded_tags=['div.main-menu', 'div.paywall', 'div.footer','[class^="player-wrapper-outer-"]'],
        # target_elements=['div.available-content','div.single-post','[class^="main-content-"]'],
        excluded_tags=['div.main-menu', 'div.paywall', 'div.footer','div.post-ufi'],
        target_elements=['div.available-content', 'div.single-post'],
        exclude_external_links=True,

        # Content processing
        process_iframes=False,
        remove_overlay_elements=True,
        check_robots_txt=True,

        # Cache control
        cache_mode=CacheMode.BYPASS,  # Use cache if available

        # Streaming when scrapping in parallel
        stream=False,

        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter() , # removes boilerplate
            options={
                "ignore_links": True,
                "skip_internal_links": True,
                "ignore_images": True,
                "escape_html": True,         # Turn HTML entities into text (default is often True).
                "body_width": 100
            }
        )
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:

        for item in articles:
            data = await get_article(item["article_link"], crawler, run_config)
            item['page']= data

        # for page in scraped_pages:
        #     print(f'\n\npage: {page["url"]} \n{page["page"]}')
        #     print('----------------------------------------------------------------------------------------------')


        #
        # RESULTS from multiple scraped pages, save original in array/file/db ?  , save the summaries in array n return these
        # format of an array ['url': <url of the scraped page>,'page':<content in markup text>]
        #


        if articles:
            for article in articles:
                prompt = """
                    # Task
                    Provide very short summary of provided article {article}.
    
                    # Requirements
                    - Keep it concise.
                    - Use a professional tone.
                """

                prompt = ChatPromptTemplate.from_template(prompt)

                chain = prompt | model | StrOutputParser()
                summary = chain.invoke({"article": article['page'][:500]})  # limiting the page text to 500 chars for speed
                article['ai_summary']=summary
        return articles



async def get_article(page_url:str, crawler, config):
    """
    Async function to get a single article content in the markdown format
    :param page_url:
    :param crawler:
    :param config:
    :return:
    """
    result = await crawler.arun(
        url=page_url,
        config=config
    )
    if result.success:
        print(result.url, " crawled OK!")

    if not result.success:
        print("Crawl failed: ", result.error_message)
        return

    return result.markdown
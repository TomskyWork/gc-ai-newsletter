# AI newsletter

## Installation 
```bash
# install python packages from requirements file
pip install --no-cache-dir -r requirements.txt

# run the crawl4ai default config - pulling headless browsers etc ...
# https://docs.crawl4ai.com/core/installation/
crawl4ai-setup
```

## Run the project

### in VS CODE
 inside the `app/` folder run the command to start the live server
 ```bash
 uvicorn main:app --reload
 ```

### in Pycharm 
- go to `app/main.py` , uncomment the 3 last lines that starts the uvicorn server when you 
press play button in the IDE   

## Browser
[http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/) - shows the API endpoints 

### Test substack scraping

go to the above 'docs' url endpoint, and use the POST request with the body

```json
{
  "scrapeSchema": "pragmatic_programmer_blog_schema",
  "url": "https://newsletter.pragmaticengineer.com/",
  "tags": []
}
```

## AWS Bedrock & Langchain
https://python.langchain.com/docs/integrations/llms/bedrock/

Amazon BEdrock Claudi AI models are only available in US or EU-Central-1

https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html

## Python Packages used

[Crawl4AI](https://docs.crawl4ai.com/) - LLM friendly scraper, crawler

[FastAPI](https://fastapi.tiangolo.com/) - API framework

[Uvicorn](https://www.uvicorn.org/) - Async server

[Langchain](https://www.langchain.com/) - AI agentic framework

Langchain-aws - used to connect to AWS Bedrock 

## Bedrock model profiles

https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html



## Docker (not working currently - can't pull the packages , certs issue)

```bash
# build docker image
docker build -t fastapi-app .

# run docker
docker run -d -p 8000:8000 fastapi-app
```
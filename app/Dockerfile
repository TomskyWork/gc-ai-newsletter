FROM python:3.13-slim

RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# runs the craw4ai lib setup which will install chromium browser
RUN crawl4ai-setup

COPY . .

# starts the uvicorn server at the start - runs the fastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
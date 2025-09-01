import boto3
import datetime

def save_article(article,settings):

    session = boto3.Session()
    dynamodb = session.resource('dynamodb', region_name=settings.aws_region)

    table = dynamodb.Table('ai-newsletter')

    table.put_item(
        Item={
            'article_title': article['article_title'],
            'date_scraped': str(datetime.date.today()),
            'article_date': article['article_date'],
            'article_link': article['article_link'],
            'article_content': str(article['page']),
            'article_summary': article['ai_summary'],
            'tags': [],
            # ... more attributes ...
        }
    )
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    date: str
    link: str

substack_article_list_schema = {
    "title": "Substack Articles",
    "baseSelector": "div[role]",    # Repeated elements  'div[role="navigation"]'
    "fields": [
        {
            "name": "article_title",
            "selector": "a[href]",
            "type": "text"
        },
        {
            "name": "article_date",
            "selector": "time[datetime]",
            "type": "attribute",
            "attribute": "datetime",
        },
        {
            "name": "article_link",
            "selector": "a[href]",
            "type": "attribute",
            "attribute": "href",
        },
    ]
}
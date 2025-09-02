from pydantic import BaseModel

#TODO is this needed?
class Article(BaseModel):
    title: str
    date: str
    link: str

pragmatic_programmer_article_list_schema = {
    "title": "Pragmatic Programmer Articles",
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

troy_hunt_list_schema = {
"title": "Troy Hunt Articles",
    "baseSelector": "div.article",
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
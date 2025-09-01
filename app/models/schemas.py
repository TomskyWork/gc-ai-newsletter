from pydantic import BaseModel
from enum import Enum
from typing import List

class SchemaEnum(str, Enum):
    pragmatic_programmer_blog_schema = 'pragmatic_programmer_blog_schema'
    unspecified_schema = 'unspecified_schema'

class ScrapeRequest(BaseModel):
    url: str

class UrlScrapeSchema(BaseModel):
    scrapeSchema: SchemaEnum
    url: str
    tags: List[str] = []

class ScrapeAllRequest(BaseModel):
    urls: List[UrlScrapeSchema]

class DeleteDateRequest(BaseModel):
    date: str
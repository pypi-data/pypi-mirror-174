from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
# print("&ensp;" * 2)


class SearchItem(BaseModel):
    title: str
    content: str
    search_keyword: str
    url: Optional[str]
    date: Optional[str]
    img_url: Optional[str]
    source: str
    page_num: int
    page_rank: int
    author: Optional[str]
    crawltime: str = today
    
    # @validator('url')
    # def url_validator(cls, v):
    #     if not v.startswith("http"):
    #         raise ValueError("url must start with http")
    #     return v
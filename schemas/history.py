from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

    model_config = ConfigDict(populate_by_name=True)


class HistoryNewsItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    image: str | None = None
    author: str | None = None
    views: int
    publish_time: datetime = Field(..., alias="publishTime")
    view_time: datetime = Field(..., alias="viewTime")
    history_id: int = Field(..., alias="historyId")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryListResponse(BaseModel):
    list: List[HistoryNewsItem]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True)
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class FavoriteNewsItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    image: str | None = None
    author: str | None = None
    views: int
    publish_time: datetime = Field(..., alias="publishTime")
    favorite_time: datetime = Field(..., alias="favoriteTime")
    favorite_id: int = Field(..., alias="favoriteId")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class FavoriteListResponse(BaseModel):
    list: List[FavoriteNewsItem]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True)
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from utils.security import get_current_user
from utils.response import success_response
from crud import favorite, users
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteNewsItem, FavoriteListResponse

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.get_user_by_username(db, username)
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)

    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorited))

@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.get_user_by_username(db, username)
    await favorite.add_favorite(db, user.id, data.news_id)
    return success_response(message="收藏成功")


@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.get_user_by_username(db, username)
    success = await favorite.remove_favorite(db, user.id, news_id)
    if not success:
        return success_response(message="未收藏该新闻")
    return success_response(message="取消收藏成功")

@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.get_user_by_username(db, username)
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)

    # 转换数据格式
    news_list = []
    for news, favorite_time, favorite_id in rows:
        news_list.append(FavoriteNewsItem(
            id=news.id,
            title=news.title,
            description=news.description,
            image=news.image,
            author=news.author,
            views=news.views,
            publishTime=news.publish_time,
            favoriteTime=favorite_time,
            favoriteId=favorite_id
        ))
    has_more = total > page * page_size
    response_data = FavoriteListResponse(list=news_list, total=total, page=page, pageSize=page_size, hasMore=has_more)
    return success_response(message="获取收藏列表成功", data=response_data)


# 清空所有收藏
@router.delete("/clear")
async def clear_favorite(
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await users.get_user_by_username(db, username)
    count = await favorite.clear_all_favorites(db, user.id)
    return success_response(message=f"已清空 {count} 条收藏")
    
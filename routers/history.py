from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from utils.security import get_current_user
from utils.response import success_response
from crud import history, users
from schemas.history import HistoryAddRequest, HistoryNewsItem, HistoryListResponse

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    验证登录，检查是否浏览过当前新闻，浏览过更新浏览时间，未浏览过添加历史记录
    """
    user = await users.get_user_by_username(db, username)
    await history.add_or_update_history(db, user.id, data.news_id)
    return success_response(message="添加历史记录成功")


@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的浏览历史列表
    """
    user = await users.get_user_by_username(db, username)
    rows, total = await history.get_history_list(db, user.id, page, page_size)

    # 转换数据格式
    news_list = []
    for news, view_time, history_id in rows:
        news_list.append(HistoryNewsItem(
            id=news.id,
            title=news.title,
            description=news.description,
            image=news.image,
            author=news.author,
            views=news.views,
            publishTime=news.publish_time,
            viewTime=view_time,
            historyId=history_id
        ))
    has_more = total > page * page_size
    response_data = HistoryListResponse(list=news_list, total=total, page=page, pageSize=page_size, hasMore=has_more)
    return success_response(message="获取历史记录列表成功", data=response_data)


@router.delete("/remove")
async def remove_history(
    news_id: int = Query(..., alias="newsId"),
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除单条历史记录
    """
    user = await users.get_user_by_username(db, username)
    success = await history.remove_history(db, user.id, news_id)
    if not success:
        return success_response(message="未找到该历史记录")
    return success_response(message="删除历史记录成功")


@router.delete("/clear")
async def clear_history(
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    清空所有历史记录
    """
    user = await users.get_user_by_username(db, username)
    count = await history.clear_all_history(db, user.id)
    return success_response(message=f"已清空 {count} 条历史记录")
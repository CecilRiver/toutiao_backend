from sqlalchemy import select, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models.history import History
from models.news import News


# 检查是否浏览过某条新闻
async def get_history_by_user_news(
    db: AsyncSession,
    user_id: int,
    news_id: int
) -> History | None:
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 添加历史记录
async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# 更新浏览时间
async def update_view_time(db: AsyncSession, history: History) -> History:
    history.view_time = datetime.now()
    await db.commit()
    await db.refresh(history)
    return history


# 添加或更新历史记录（浏览过则更新时间，未浏览过则添加）
async def add_or_update_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    existing = await get_history_by_user_news(db, user_id, news_id)
    if existing:
        return await update_view_time(db, existing)
    return await add_history(db, user_id, news_id)


# 获取历史记录列表
async def get_history_list(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 10
):
    # 总量
    count_query = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    # 获取历史列表 -> 联表查询 + 浏览时间排序 + 分页
    query = (select(News, History.view_time.label("view_time"), History.id.label("history_id"))
            .join(History, History.news_id == News.id)
            .where(History.user_id == user_id)
            .order_by(History.view_time.desc())
            .offset(offset).limit(page_size)
            )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 删除单条历史记录
async def remove_history(db: AsyncSession, user_id: int, news_id: int) -> bool:
    query = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


# 清空所有历史记录
async def clear_all_history(db: AsyncSession, user_id: int) -> int:
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount
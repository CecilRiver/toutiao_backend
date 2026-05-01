from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.users import User
from schemas.users import UserRequest
from utils import security

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密处理 -> add
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password = hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读回最新的 user
    return user

# 验证用户并创建 token
async def authenticate_and_create_token(db: AsyncSession, username: str, password: str) -> str | None:
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return security.create_token({"sub": user.username})


# 更新用户信息
async def update_user(db: AsyncSession, username: str, update_data) -> User:
    user = await get_user_by_username(db, username)
    if not user:
        return None

    # 只更新提供的字段
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


# 修改密码
async def change_password(db: AsyncSession, username: str, old_password: str, new_password: str) -> bool:
    user = await get_user_by_username(db, username)
    if not user:
        return False

    # 验证旧密码
    if not security.verify_password(old_password, user.password):
        return False

    # 更新密码
    user.password = security.get_hash_password(new_password)
    await db.commit()
    return True
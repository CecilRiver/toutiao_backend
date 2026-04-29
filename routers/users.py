from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from schemas.users import UserRequest
from crud import users
from utils import security, response
from schemas.users import UserAuthResponse, UserInfoResponse
from utils.security import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user = await users.create_user(db, user_data)
    token = security.create_token({"sub": user.username})

    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return response.success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户名密码 -> 生成 Token -> 响应结果
    token = await users.authenticate_and_create_token(db, user_data.username, user_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    user = await users.get_user_by_username(db, user_data.username)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return response.success_response(message="登录成功", data=response_data)


@router.get("/info")
async def get_user_info(
    username: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 获取用户信息：通过 token 解析用户名 -> 查询用户信息 -> 响应结果
    user = await users.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    response_data = UserInfoResponse.model_validate(user)
    return response.success_response(message="获取成功", data=response_data)
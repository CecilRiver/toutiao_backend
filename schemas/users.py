from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: int
    username: str
    bio: str
    avatar: str

class UserResponse(BaseModel):
    code: int = 200
    message: str = "注册成功"
    data: dict

    class Config:
        from_attributes = True
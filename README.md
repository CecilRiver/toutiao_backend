# AI掘金头条后端

基于 FastAPI 的新闻资讯系统后端 API。

## 技术栈

- **Web 框架**: FastAPI 0.135+
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **数据库**: MySQL (aiomysql)
- **认证**: JWT (PyJWT)
- **密码加密**: Passlib + bcrypt

## 项目结构

```
toutiao_backend/
├── config/         # 配置模块（数据库、settings）
├── crud/           # 数据库操作层
├── models/         # ORM 模型
├── routers/        # API 路由
├── schemas/        # Pydantic 模型（请求/响应）
├── utils/          # 工具模块（security）
└── main.py         # 应用入口
```

## 快速开始

1. 安装依赖：
```bash
uv sync
```

2. 配置环境变量（复制 `.env.example` 为 `.env`）：
```bash
cp .env.example .env
```

3. 启动开发服务器：
```bash
uv run fastapi dev main.py
```

4. 访问 API 文档：http://localhost:8000/docs

## 接口进度

### 用户模块 `/api/user`

| 接口 | 方法 | 状态 |
|------|------|------|
| 注册 | POST /register | ✅ 已完成 |
| 登录 | POST /login | ⏳ 待完成 |
| 获取用户信息 | GET /info | ⏳ 待完成 |
| 更新用户信息 | PUT /update | ⏳ 待完成 |
| 修改密码 | PUT /password | ⏳ 待完成 |

### 新闻模块 `/api/news`

| 接口 | 方法 | 状态 |
|------|------|------|
| 分类列表 | GET /categories | ✅ 已完成 |
| 新闻列表 | GET /list | ✅ 已完成 |
| 新闻详情 | GET /detail | ✅ 已完成 |

### 收藏模块 `/api/favorite`

| 接口 | 方法 | 状态 |
|------|------|------|
| 检查收藏状态 | GET /check | ⏳ 待完成 |
| 添加收藏 | POST /add | ⏳ 待完成 |
| 取消收藏 | DELETE /remove | ⏳ 待完成 |
| 收藏列表 | GET /list | ⏳ 待完成 |
| 清空收藏 | DELETE /clear | ⏳ 待完成 |

### 浏览历史模块 `/api/history`

| 接口 | 方法 | 状态 |
|------|------|------|
| 添加浏览记录 | POST /add | ⏳ 待完成 |
| 浏览历史列表 | GET /list | ⏳ 待完成 |
| 删除浏览记录 | DELETE /delete/{id} | ⏳ 待完成 |
| 清空浏览历史 | DELETE /clear | ⏳ 待完成 |

## 环境变量

| 变量 | 说明 |
|------|------|
| DB_HOST | 数据库地址 |
| DB_PORT | 数据库端口 |
| DB_NAME | 数据库名 |
| DB_USER | 数据库用户名 |
| DB_PASSWORD | 数据库密码 |
| SECRET_KEY | JWT 密钥 |
| ALGORITHM | JWT 算法 (默认 HS256) |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token 过期时间 |
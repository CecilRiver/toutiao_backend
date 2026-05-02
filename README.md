# AI掘金头条后端

基于 FastAPI 的新闻资讯系统后端 API。

## 技术栈

- **Web 框架**: FastAPI 0.135+
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **数据库**: MySQL (aiomysql)
- **缓存**: Redis (redis-py 异步模式)
- **认证**: JWT (PyJWT)
- **密码加密**: Passlib + bcrypt

## 项目结构

```
toutiao_backend/
├── config/         # 配置模块（数据库、Redis、settings）
├── cache/          # 缓存操作层
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
| 登录 | POST /login | ✅ 已完成 |
| 获取用户信息 | GET /info | ✅ 已完成 |
| 更新用户信息 | PUT /update | ✅ 已完成 |
| 修改密码 | PUT /password | ✅ 已完成 |

### 新闻模块 `/api/news`

| 接口 | 方法 | 状态 |
|------|------|------|
| 分类列表 | GET /categories | ✅ 已完成 |
| 新闻列表 | GET /list | ✅ 已完成 |
| 新闻详情 | GET /detail | ✅ 已完成 |

### 收藏模块 `/api/favorite`

| 接口 | 方法 | 状态 |
|------|------|------|
| 检查收藏状态 | GET /check | ✅ 已完成 |
| 添加收藏 | POST /add | ✅ 已完成 |
| 取消收藏 | DELETE /remove | ✅ 已完成 |
| 收藏列表 | GET /list | ✅ 已完成 |
| 清空收藏 | DELETE /clear | ✅ 已完成 |

### 浏览历史模块 `/api/history`

| 接口 | 方法 | 状态 |
|------|------|------|
| 添加浏览记录 | POST /add | ✅ 已完成 |
| 浏览历史列表 | GET /list | ✅ 已完成 |
| 删除浏览记录 | DELETE /remove | ✅ 已完成 |
| 清空浏览历史 | DELETE /clear | ✅ 已完成 |

## 环境变量

| 变量 | 说明 |
|------|------|
| DB_HOST | 数据库地址 |
| DB_PORT | 数据库端口 |
| DB_NAME | 数据库名 |
| DB_USER | 数据库用户名 |
| DB_PASSWORD | 数据库密码 |
| REDIS_HOST | Redis 地址 |
| REDIS_PORT | Redis 端口 |
| REDIS_DB | Redis 数据库编号 (0-15) |
| REDIS_PASSWORD | Redis 密码 |
| SECRET_KEY | JWT 密钥 |
| ALGORITHM | JWT 算法 (默认 HS256) |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token 过期时间 |

## 缓存设计

### 缓存策略

采用 Redis 作为缓存层，缓存热点数据以减少数据库查询压力。

| 数据类型 | 缓存 Key | 过期时间 | 说明 |
|----------|----------|----------|------|
| 新闻分类 | `news:categories` | 7200s (2h) | 分类数据稳定，缓存时间较长 |


### 缓存模块

- `config/cache_conf.py`: Redis 连接配置与基础缓存操作
- `cache/news_cache.py`: 新闻相关缓存操作封装
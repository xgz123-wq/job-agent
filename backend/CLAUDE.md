# fastapi-scaffold 项目配置

## 项目概述

通用 AI 后端脚手架：三层架构 + PG + Redis + Celery + JWT + Alembic + 统一响应 + 双端路由 + AI 通用封装（chat/complete/SSE）。

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | FastAPI (async) |
| 数据库 | PostgreSQL + SQLAlchemy async |
| 缓存/队列 | Redis |
| 异步任务 | Celery (worker + beat) |
| 数据库迁移 | Alembic |
| 鉴权 | JWT (access + refresh) |
| AI 服务 | DeepSeek/OpenAI 兼容封装 |
| 反向代理 | Nginx（envsubst 模板） |
| 部署 | Docker Compose |

## 项目结构

```
fastapi-scaffold/
├── app/
│   ├── api/            # 路由接口层（client/backoffice 双端）
│   ├── services/       # 业务逻辑层（client/backoffice/common）
│   ├── models/         # SQLAlchemy ORM（user/token/admin）
│   ├── schemas/        # Pydantic 请求/响应模型
│   ├── db/             # 数据库引擎、session
│   ├── core/           # 配置、安全、Celery、日志
│   ├── route/          # 路由注册中心 router_registry
│   ├── schedule/       # 定时任务
│   ├── configs/        # Swagger 配置、文档应用工厂
│   └── common/         # 通用工具/常量
├── migrations/         # Alembic 迁移
├── nginx/              # nginx.conf.template（envsubst）
├── scripts/            # 管理脚本
└── docker-compose*.yml # 多环境编排
```

## 分层架构规则

```
api（接收请求、参数校验、鉴权注入、调用 service、返回统一响应）
  ↓ 调用
services（核心业务逻辑，不直接处理 HTTP）
  ↓ 调用
db/models（数据访问，仅 service 层可调用 db）
```

- **禁止跨层调用**：api 不能直接访问 db/models
- **禁止反向依赖**：models/schemas 不依赖 api/services
- **统一响应**：所有接口通过 `ApiResponse` 包装

## 关键业务链路

- 通用 AI 对话：`app/api/client/v1/ai.py` → `app/services/client/ai_service.py`
- 认证流程：`app/api/client/v1/auth.py` → `app/services/client/auth.py` → `app/core/security.py`
- 数据访问：`app/db/base.py`（引擎） → `app/db/session.py`（session） → `app/models/`（ORM）
- 路由注册：`app/route/router_registry.py`（CLIENT_ROUTES + BACKOFFICE_ROUTES）

## 常用命令

```bash
# 启动所有服务
docker compose up -d --build

# 开发模式（热重载，禁用 nginx）
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# 数据库迁移
docker compose exec app alembic upgrade head
docker compose exec app alembic revision --autogenerate -m "描述"

# 初始化管理员
docker compose exec app python -m app.scripts.seed_admin

# 运行测试
docker compose exec app pytest

# 脚手架验收
bash scripts/verify-scaffold.sh
```

## 注意事项

- `.env` 不提交，参考 `.env.example` 配置；`.env` 与 `.env.example` 双向同步
- 通用 AI 路由用 SSE（Server-Sent Events），系统级 Nginx 需 `proxy_buffering off`
- `client` 和 `backoffice` 两套路由，鉴权策略分离
- 所有 AI 调用封装在 `app/services/client/ai_service.py`，不在 api 层直接调用
- 端口/容器名/网络名全 `.env` 参数化：`PROJECT_NAME` / `API_PORT` / `POSTGRES_*` / `REDIS_*` / `NGINX_*`
- 生产环境启动校验：`SECRET_KEY` 必须修改默认值、`CORS_ALLOWED_ORIGINS` 必须显式配置
- nginx 配置用 envsubst 模板（`nginx/nginx.conf.template`），`API_PORT`/`SERVER_NAME` 在容器启动时渲染

# FastAPI Scaffold

> 通用 AI 后端脚手架：三层架构 + PostgreSQL + Redis + Celery + JWT + Alembic + 统一响应 + 双端路由 + AI 通用封装 + SSE 流式。

## 定位

从生产级 AI 应用沉淀的通用后端模板，开箱即用 JWT 鉴权、双端路由（client/backoffice）、Celery 异步任务、SSE 流式 AI 对话，业务侧只需在 `app/services/` 增量写业务逻辑即可。

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | FastAPI (async) |
| 数据库 | PostgreSQL + SQLAlchemy async |
| 缓存/队列 | Redis |
| 异步任务 | Celery (worker + beat) |
| 数据库迁移 | Alembic |
| 鉴权 | JWT (access_token + refresh_token) |
| AI 服务 | DeepSeek/OpenAI 兼容接口封装 |
| 反向代理 | Nginx（envsubst 模板） |
| 部署 | Docker Compose (app/postgres/redis/celery/nginx) |

## 快速启动

```bash
# 1. 复制环境配置
cp .env.example .env

# 2. 按需修改 .env（PROJECT_NAME / API_PORT / POSTGRES_* / SECRET_KEY 等）

# 3. 启动全部服务
docker compose up -d --build

# 4. 执行数据库迁移
docker compose exec app alembic upgrade head

# 5. 初始化管理员（可选）
docker compose exec app python -m app.scripts.seed_admin
```

启动后访问：
- API 文档（client）：http://localhost:${NGINX_HTTP_PORT:-8080}/docs
- 后台文档（backoffice）：http://localhost:${NGINX_HTTP_PORT:-8080}/backoffice/docs
- 健康检查：http://localhost:${NGINX_HTTP_PORT:-8080}/health

开发模式（热重载，禁用 nginx）：

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

生产模式（使用预构建镜像，禁用 docker 内 nginx）：

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 目录结构

```
fastapi-scaffold/
├── app/
│   ├── api/              # 路由接口层（client/backoffice 双端）
│   │   ├── client/v1/    # 用户端路由（auth/demo/config/aws/ai）
│   │   └── backoffice/v1/ # 后台路由（auth/admin/users/aws）
│   ├── services/         # 业务逻辑层
│   │   ├── client/       # 用户端业务（ai_service/auth/email_templates/redis_verification）
│   │   ├── backoffice/   # 后台业务（admin/auth）
│   │   └── common/       # 公共服务（email_smtp/email_brevo/redis/thread_pool）
│   ├── models/           # SQLAlchemy ORM（user/token/admin）
│   ├── schemas/          # Pydantic 请求/响应模型
│   ├── db/               # 数据库引擎、session
│   ├── core/             # 配置、安全、Celery、日志
│   ├── route/            # 路由注册中心（router_registry）
│   ├── schedule/         # 定时任务（Celery beat + APScheduler）
│   ├── configs/          # Swagger 配置、文档应用工厂
│   ├── common/           # 通用工具（release/language/log_consumer）
│   └── exceptions/       # 异常定义
├── migrations/           # Alembic 迁移脚本
├── nginx/                # nginx.conf.template（envsubst 模板）
├── resources/emails/     # 邮件模板
├── scripts/              # 管理脚本
├── tests/                # 测试
├── docker-compose*.yml   # 多环境编排
├── Dockerfile*           # 生产/开发镜像
├── alembic.ini
├── requirements.txt
└── .env.example          # 环境变量样例（.env 不入 git）
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
- **统一响应**：所有接口通过 `ApiResponse` 包装，区分 HTTP code 和业务 code

## .env 关键配置

完整变量见 `.env.example`，关键项：

| 变量 | 说明 | 默认 |
|------|------|------|
| `PROJECT_NAME` | 项目名（驱动 container_name/network name） | `fastapi-scaffold` |
| `API_PORT` | 应用监听端口 | `8001` |
| `POSTGRES_PORT` / `POSTGRES_HOST` | PG 主机端口 / 容器内服务名 | `5434` / `postgres` |
| `REDIS_PORT` / `REDIS_EXTERNAL_PORT` | Redis 容器内/主机端口 | `6379` / `6382` |
| `NGINX_HTTP_PORT` / `NGINX_HTTPS_PORT` | Nginx 主机端口 | `8080` / `8443` |
| `SERVER_NAME` | Nginx server_name | `localhost` |
| `CORS_ALLOWED_ORIGINS` | 生产环境 CORS（逗号分隔，生产必填） | 空 |
| `SECRET_KEY` | JWT 密钥（生产强制修改默认值） | 占位串 |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | 占位串 |

## 常用命令

```bash
# 启动全部服务
docker compose up -d

# 查看日志
docker compose logs -f app

# 进入容器
docker compose exec app bash

# 数据库迁移
docker compose exec app alembic upgrade head
docker compose exec app alembic revision --autogenerate -m "描述"

# 运行测试
docker compose exec app pytest

# 停止并清理
docker compose down
```

## 通用 AI 路由

脚手架内置与业务无关的 AI 对话能力（`app/api/client/v1/ai.py`）：

- `POST /api/v1/ai/chat` — 非流式对话补全
- `POST /api/v1/ai/chat/complete` — 结构化 JSON 输出补全
- `POST /api/v1/ai/chat/stream` — SSE 流式对话补全

请求体参数：`system_prompt` / `user_prompt` / `model` / `temperature` / `max_tokens` / `history`。

## License

MIT

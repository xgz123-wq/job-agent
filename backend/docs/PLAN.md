# fastapi-scaffold 脚手架迁移计划

> TL;DR: 从 ai-interview 后端抽离通用 AI 后端脚手架，端口/容器名/项目名全 .env 化，留 JWT 最小 demo，删面试专属业务，独立仓库 + v1.0.0 tag。经 subagent (GLM-5.2) 逐条核对实际代码，合并 25 项遗漏修正。

## 决策对齐（grilling 结论）

| 决策点 | 选择 | 含义 |
|---|---|---|
| Q1 剥离程度 | B | AI 应用脚手架：三层架构+PG+Redis+Celery+JWT+Alembic+统一响应+双端路由+AI 通用封装+SSE+prompt 结构化 |
| Q2 业务样例 | b | 留 `user.py`+`token.py`+`auth.py` 开箱 JWT；删 interview/resume/interview_message/waiting_list |
| Q3 端口参数化 | a | 全 .env 化，yaml 用 `${VAR:-default}`，nginx 用 envsubst；`PROJECT_NAME=fastapi-scaffold`；.env 与 .env.example 双向同步 |
| Q4 仓库策略 | c | 独立新仓库 `fastapi-scaffold/`（扁平式）；原 ai-interview 保留不动；打 `v1.0.0` tag |
| Q5 计划文档 | b | 任务级粒度；写到新仓库 `docs/PLAN.md`；加 T7 自动化验收 `scripts/verify-scaffold.sh`；checkbox 进度标记 |

## 仓库策略

- 仓库根：`D:\AGI大模型\AI-project\fastapi-scaffold\`（扁平式，无 backend/ 包裹）
- 源仓库：`D:\AGI大模型\AI-project\ai-interview\ai-interview-backend\`（复制干净文件，原仓库不动）
- 原仓库 `ai-interview/` 保留不动，与新仓库互不干扰
- 版本控制：`.env` / `uploads/` / `logs/` / `__pycache__/` 入 `.gitignore`；`.env.example` 入 git
- tag：全部任务完成后打 `v1.0.0`

## 任务清单

> 每个任务标注「原计划」与「核对追加」两部分。核对追加来自 subagent 审查的 25 条问题（见文末审查核对表）。

### T1 端口参数化 + 网络与连通性修复

**原计划：**
- [ ] 改 `docker-compose.yml`：postgres 端口 `${POSTGRES_PORT:-5434}:5432`、redis `${REDIS_PORT:-6382}:6379`、nginx `${NGINX_HTTP_PORT:-8080}:80` `${NGINX_HTTPS_PORT:-8443}:443`、flower `${FLOWER_PORT:-5555}:5555`
- [ ] 改 `docker-compose.dev.yml` / `docker-compose.prod.yml`：同步端口参数化
- [ ] 改 `nginx/prepwise.conf` → `nginx/app.conf.template`：用 envsubst 模板，`proxy_pass http://localhost:${API_PORT}`、`server_name ${SERVER_NAME}`
- [ ] 补 `.env.example`：加 `NGINX_HTTP_PORT/NGINX_HTTPS_PORT/FLOWER_PORT/REDIS_EXTERNAL_PORT/PROJECT_NAME/SERVER_NAME/CORS_ORIGINS`，分组注释
- [ ] 同步 `.env`（本地开发用，不入 git）

**核对追加（必须修）：**
- [ ] **#1 修 docker-compose.yml app 服务缺 networks**：app 服务当前未挂 `app-network`，与 postgres/redis 网络隔离 → 容器间 DNS 不通。在 app 服务 healthcheck 后追加 `networks: - app-network`
- [ ] **#2 修健康检查端口写死 8006**：docker-compose.yml L16 硬编码 `localhost:8006`，与 config.py 默认 8001、.env.example 8006 三处不一致 → 改 `${API_PORT:-8001}`，参照 prod.yml L13 已正确写法
- [ ] **#3 修 POSTGRES_HOST 默认局域网 IP**：config.py L26 `POSTGRES_HOST = "192.168.110.90"` → 改 `"postgres"`（Docker 内用服务名）
- [ ] **#4 修 REDIS_HOST 默认 localhost**：config.py L33 `REDIS_HOST = "localhost"` → 改 `"redis"`（容器内 localhost 指向自身）
- [ ] **#5 nginx.conf 也参数化（不只 prepwise.conf）**：docker-compose.yml L84 实际挂的是 `nginx/nginx.conf` 不是 prepwise.conf；nginx.conf L33/L46 硬编码 `proxy_pass http://app:8001` → 改用 envsubst 模板 `nginx/nginx.conf.template`，entrypoint 渲染 `${API_PORT}`
- [ ] **#13 统一 config.py 端口默认值与 compose**：config L13-16 默认 6386/8086/8446/5556 vs compose 实际 6382/8080/8443/5555 → 对齐为 6382/8080/8443/5555

**核对追加（应该修）：**
- [ ] #6 Dockerfile EXPOSE 8001：仅元数据，HEALTHCHECK 已参数化，低优先级，可选改 `ARG API_PORT=8001` + `EXPOSE ${API_PORT}`
- [ ] #21 删除 docker-compose.yml L85 的 `./ssl:/etc/nginx/ssl` 幽灵挂载（项目无 ssl 目录），或新建 `ssl/.gitkeep` 占位
- [ ] #25 修 celerybeat-schedule.db 挂载：当前挂成目录导致 celery beat 写状态失败 → 改用命名卷 `celerybeat-data:/app/celerybeat-schedule.db`，并在 volumes 顶层声明

**验收**：改 `.env` 的 `API_PORT/POSTGRES_PORT/REDIS_PORT/NGINX_HTTP_PORT/PROJECT_NAME` 后，`docker compose config` 输出反映新值；nginx 容器启动后 `proxy_pass` 指向新 `API_PORT`；`docker compose up -d` 后 app 与 postgres/redis 网络连通（app 容器内 `ping postgres` 通）。

---

### T2 业务代码清理（B + b 方案）

**原计划：**
- [ ] 删 `app/models/{interview,resume,interview_message,waiting_list}.py`
- [ ] 删 `app/services/client/{interview_service,resume_service,waiting_list}.py`
- [ ] 删 `app/api/client/v1/` 下 interview/resume/waiting_list 路由文件
- [ ] 删 `app/schemas/client/` 或 `backoffice/` 下对应 interview/resume/waiting_list schema
- [ ] 清理 `app/models/__init__.py`、`app/services/client/__init__.py`、`app/api/__init__.py` 的 import
- [ ] 删 `migrations/versions/` 下面试迁移
- [ ] 删 `app/scripts/seed_admin.py` 中面试业务数据（保留 admin 创建逻辑）

**核对追加（必须修）：**
- [ ] **#14 删 backoffice 侧面试文件**：`app/api/backoffice/v1/{interviews,waiting_list}.py`、`app/services/backoffice/waiting_list.py`
- [ ] **#15 清理 router_registry.py**：CLIENT_ROUTES 删 3 条（waiting_list L52、resume L60、interview L68），BACKOFFICE_ROUTES 删 2 条（waiting_list L66、interviews L74），保留 auth/demo/config/aws/admin/users
- [ ] **#12 修 Dockerfile 装 MySQL 库**：L14-19 `default-libmysqlclient-dev` → 换 `libpq-dev`（PostgreSQL 客户端库）
- [ ] **#11 清 requirements.txt 面试依赖**：删 `pypdf2/python-docx/pandas/numpy/lxml/pdfplumber`（简历解析专用）

**核对追加（应该修）：**
- [ ] #19 删 `uploads/resumes/` 目录（面试专属），只保留 `uploads/avatars/`
- [ ] #20 删 `resources/emails/auth/` 下 `waiting_list_admin_notification.html`、`waiting_list_verification.html` 2 个模板，保留通用 3 个
- [ ] #24 评估 `app/db/models.py`（仅 3 行 Base 声明）合并进 `app/db/base.py`，消除与 `app/models/` 的命名混淆；或保留加注释

**验收**：`from app.models import` 只剩 `base/user/token/admin`；`from app.services.client import` 只剩 `ai_service/auth/email_templates/redis_verification`；`docker compose up` 后 `/api/v1/health` 返回 200；`pytest` 过；`grep -ri "interview\|resume\|waiting_list\|pypdf2\|libmysqlclient" app/ requirements.txt Dockerfile` 无残留。

---

### T3 AI 通用能力保留与清洗

**原计划：**
- [ ] 改 `app/services/client/ai_service.py`：去面试 prompt 硬编码，改为通用 `chat()` / `complete()` 抽象，支持传入 `system_prompt` / `user_prompt` / `model` / `stream` 参数
- [ ] 保留 SSE 流式能力：通用 `/api/v1/ai/chat/stream` 路由（参数化 prompt，不绑面试场景）
- [ ] 保留 prompt 结构化 JSON 输出约束（通用 system_prompt 模板，不硬编码面试字段）
- [ ] 删面试专属 prompt（出题、评分、简历解析）

**核对追加（应该修）：**
- [ ] #18 清 `app/services/client/email_templates.py`：L51 `dashboard_url="https://prepwise.com/dashboard"` → 改 `settings.FRONTEND_URL + "/dashboard"`；删 import 的 `send_waiting_list_*` 函数及对应方法
- [ ] #22 清 `app/schedule/jobs/email_tasks.py`：删 `send_waiting_list_verification_task` 任务；`demo.py` 通用无面试逻辑，保留

**验收**：`ai_service` 支持传入 `system_prompt` 参数；`grep -ri "interview\|resume\|出题\|评分\|prepwise" app/services/client/ai_service.py app/services/client/email_templates.py app/schedule/jobs/` 无残留。

---

### T4 项目标识参数化 + 安全加固

**原计划：**
- [ ] 改 `docker-compose.yml`：所有 `container_name: ai-interview-*` → `${PROJECT_NAME:-fastapi-scaffold}-*`
- [ ] 改 networks/volumes 名：`app-network` → `${PROJECT_NAME:-fastapi-scaffold}-network`
- [ ] 改 `app/core/config.py` 默认值：`PROJECT_NAME="FastAPI Scaffold"`、`ADMIN_EMAIL` 改中性默认、`MAIL_FROM_NAME` 清 `Seiki`/`FastAPI Template` 残留
- [ ] 改 `nginx` server_name 用 `${SERVER_NAME}` 模板
- [ ] 改 logs 路径、健康检查 URL 跟随 `API_PORT`
- [ ] 全局 grep 清除 `ai-interview` / `prepwise` / `Prepwise` / `智面` 业务字样

**核对追加（应该修）：**
- [ ] #7 改 docker-compose.prod.yml 镜像默认值：4 处 `ghcr.io/dev-zetos/prepwise-app:latest` → `${IMAGE_TAG:-fastapi-scaffold-app:latest}`
- [ ] #8 改 docker-compose.dev.yml 镜像名：3 处 `ai-interview:dev` → `${IMAGE_TAG:-fastapi-scaffold:dev}`
- [ ] #9 修 CORS 生产 `["*"]`：route.py L26-29 + docs_apps.py L24-26 两处生产分支也是 `["*"]` → 改 `settings.CORS_ALLOWED_ORIGINS`；config.py 新增 `CORS_ALLOWED_ORIGINS: list = []`，.env.example 加 `CORS_ORIGINS`
- [ ] #10 加 SECRET_KEY 启动校验：config.py `__init__` 末尾加 `if ENV=="production" and SECRET_KEY.startswith("your-secret-key"): raise RuntimeError(...)`
- [ ] #16 清 swagger 品牌文案：`app/configs/client_swagger_config.py` 描述删 `### Waiting List Management` 段；`.env.example` 的 `PROJECT_NAME=AI-Interview` → `PROJECT_NAME=fastapi-scaffold`
- [ ] #17 改 `app/common/release.py`：硬编码 2020 年时间戳 + `0.1.0` → 改为从 `settings` 或 `__version__` 读取，时间戳留空或由 CI 注入
- [ ] #23 改 `app/api/docs_export.py` L51/L65 硬编码 `"FastAPI Template - API文档导出功能"` → `f"{settings.PROJECT_NAME} - API文档导出功能"`

**验收**：改 `PROJECT_NAME` 后所有容器名/网络名/卷名同步；`grep -ri "ai-interview\|prepwise\|Prepwise\|智面\|dev-zetos\|Seiki" app/ nginx/ docker-compose*.yml .env.example` 无业务残留（历史迁移文件注释可留）；生产环境启动若 `SECRET_KEY` 未改会报错；CORS 生产环境读 `.env`。

---

### T5 文档重写

**原计划：**
- [ ] 重写 `README.md`：脚手架说明（定位、技术栈、快速启动、目录结构、.env 配置说明）
- [ ] 重写 `部署文档.md`：通用版，删 ai-interview 业务描述，命令示例与 T1-T4 参数化后一致
- [ ] 重写 `CLAUDE.md`：指向新仓库结构，更新技术栈/常用命令/分层架构规则，控制在 100 行内
- [ ] 同步更新 `.env.example` 顶部注释

**验收**：文档无 `ai-interview`/`PrepWise`/`智面` 业务字样；命令示例与参数化后一致；`docker compose up -d` 按文档命令可跑通。

---

### T6 版本控制基线

- [x] 在 `fastapi-scaffold/` 执行 `git init`（已完成）
- [x] 写 `.gitignore`：排除 `.env` / `uploads/` / `logs/` / `__pycache__/` / `celerybeat-schedule.db*` / `.venv/`（已完成）
- [x] 首个 commit：`脚手架基线: 从 ai-interview 抽离的通用 AI 后端模板`（已完成 b55417c）
- [ ] 各任务完成按原子提交（commit message 简短中文 + 技术术语保留英文）
- [ ] 全部任务完成后打 tag `v1.0.0`

**验收**：`git log --oneline` 显示基线提交与各任务提交；`git tag -l` 显示 `v1.0.0`；`.gitignore` 正确排除敏感文件。

---

### T7 验收脚本

- [ ] 写 `scripts/verify-scaffold.sh`：
  - 检查 `docker compose config` 端口参数化生效（API_PORT/POSTGRES_*/REDIS_*/NGINX_HTTP_PORT/PROJECT_NAME 均用 `${VAR}` 形式）
  - 检查 `docker compose config` 的 app 服务有 `networks` 字段
  - 检查 `grep -ri "ai-interview\|prepwise\|智面\|dev-zetos\|Seiki"` 无业务残留
  - 检查 `from app.models import` 只剩 `base/user/token/admin`
  - 检查 `from app.services.client import` 只剩 `ai_service/auth/email_templates/redis_verification`
  - 检查 `.env.example` 含所有必需变量（API_PORT/POSTGRES_*/REDIS_*/NGINX_HTTP_PORT/PROJECT_NAME/SERVER_NAME/CORS_ORIGINS）
  - 检查 `requirements.txt` 不含 pypdf2/python-docx/pandas/numpy/lxml/pdfplumber
  - 检查 `Dockerfile` 不含 libmysqlclient
  - 运行 `pytest`
- [ ] 脚本可重复执行，输出 PASS/FAIL 清单

**验收**：`bash scripts/verify-scaffold.sh` 全部 PASS。

---

## 审查核对表（subagent GLM-5.2 逐条核对，2026-07-24）

> Qwen 审查提出 25 个问题，subagent 逐条核对实际代码后**全部确认属实**。按修复优先级三档分类。

### 必须修（阻塞部署 / 安全 / 连通性，6 条）

| # | 问题 | 位置 | 说明 |
|---|------|------|------|
| 1 | app 服务缺 networks | docker-compose.yml L4-19 | 未挂 app-network，与 pg/redis 网络隔离，容器间 DNS 不通 |
| 3 | POSTGRES_HOST 默认局域网 IP | config.py L26 | `192.168.110.90` 是作者本机 IP，Docker 内应 `postgres` |
| 4 | REDIS_HOST 默认 localhost | config.py L33 | 容器内 localhost 指向自身，连不到 redis 服务 |
| 9 | CORS 生产也是 ["*"] | route.py L26-29, docs_apps.py L24-26 | 两个分支都是 ["*"]，生产留 TODO 未改 |
| 12 | Dockerfile 装 MySQL 库 | Dockerfile L14-19 | `default-libmysqlclient-dev`，项目用 PG，应换 `libpq-dev` |
| 25 | celerybeat-schedule.db 挂成目录 | docker-compose.yml L51 | 文件不存在被 Docker 创建为空目录，celery beat 写状态失败 |

### 应该修（影响通用性/正确性，13 条）

| # | 问题 | 位置 | 说明 |
|---|------|------|------|
| 2 | 健康检查写死 8006 | docker-compose.yml L16 | 与 config 默认 8001、.env 8006 三处不一致 |
| 5 | nginx.conf 硬编码 app:8001 | nginx.conf L33/L46 | compose 挂的是 nginx.conf 不是 prepwise.conf |
| 7 | prod.yml 4 处 prepwise 镜像 | docker-compose.prod.yml L7 | `ghcr.io/dev-zetos/prepwise-app:latest` 默认值 |
| 8 | dev.yml 3 处 ai-interview:dev | docker-compose.dev.yml L18 | 无 env 覆盖 |
| 10 | SECRET_KEY 占位串 | config.py L66 | 缺生产校验，忘改 .env 即用此串签 JWT |
| 11 | requirements 含面试依赖 | requirements.txt | pypdf2/python-docx/pandas/numpy/lxml/pdfplumber |
| 13 | 端口默认值错位 | config.py L13-16 | 6386/8086/8446/5556 vs compose 实际 6382/8080/8443/5555 |
| 14 | backoffice 面试文件 | api/backoffice/v1/, services/backoffice/ | interviews.py, waiting_list.py 待删 |
| 15 | 路由表 5 条面试业务 | router_registry.py L52-74 | client 删 3 条，backoffice 删 2 条 |
| 16 | swagger 含品牌文案 | client_swagger_config.py L52-61 | 描述含 `### Waiting List Management` 段 |
| 18 | email_templates 含 PrepWise | email_templates.py L51 | `https://prepwise.com/dashboard` + waiting_list 方法 |
| 20 | resources/emails 含面试模板 | resources/emails/auth/ | 2 个 waiting_list_*.html |
| 22 | email_tasks.py 含面试任务 | schedule/jobs/email_tasks.py | `send_waiting_list_verification_task` |

### 不需要改（影响小/已较干净，6 条）

| # | 问题 | 说明 |
|---|------|------|
| 6 | Dockerfile EXPOSE 8001 | 仅元数据，HEALTHCHECK 已参数化 |
| 17 | release.py 时间戳 | 仅版本展示，不阻塞（可选改） |
| 19 | uploads/resumes | 空目录，删否随意 |
| 21 | ./ssl 挂载 | 空目录无害，可保留占位 |
| 23 | docs_export 字符串 | 已是通用名 "FastAPI Template" |
| 24 | app/db/models.py 双路径 | 仅 Base 声明，单一定义，非真重复（可选合并注释） |

---

## 执行顺序

T1（端口+网络）→ T2（删业务）→ T3（AI+邮件清洗）→ T4（标识参数化+安全）→ T5（文档）→ T6（版本控制，贯穿全程）→ T7（验收）

每个任务完成后勾选 checkbox，提交一次原子 commit。T6 的 `git init` 已完成，tag 在全部完成后打。

## 进度追踪

- [x] 计划文档定稿
- [x] subagent 核对 25 条遗漏（全部属实）
- [x] T1 端口参数化 + 网络与连通性修复
- [x] T2 业务代码清理
- [x] T3 AI 通用能力 + 邮件清洗
- [x] T4 项目标识参数化 + 安全加固
- [x] T5 文档重写
- [x] T6 版本控制基线（git init + 首个 commit 已完成，各任务原子 commit 完成）
- [x] T7 验收脚本（scripts/verify-scaffold.sh 全 PASS）
- [x] 打 tag v1.0.0

## 回滚策略

- 每个任务独立 commit，不满意可 `git reset --hard <commit>` 回滚
- 原 ai-interview 仓库不动，最坏情况重新从源仓库复制

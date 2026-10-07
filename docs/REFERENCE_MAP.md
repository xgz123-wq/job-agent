# 代码地图：哪个文件对应哪个功能

分两部分。第一部分是你自己的后端脚手架，这是项目的身体。第二部分是参考项目，用来学智能体那几块怎么写。

行数和路径是 2026-10-07 实际核对过的。

## 第一部分：backend/（你的 fastapi-scaffold）

### 一个请求走过的路

以「登录」为例，按这个顺序读，就认识了整个后端。阶段 0 让教练带你走一遍。

| 顺序 | 文件 | 行数级别 | 它在这条路上干什么 |
| --- | --- | --- | --- |
| 1 | `main.py` | 20 | 程序入口，创建应用 |
| 2 | `app/route/router_registry.py` | 短 | 所有接口在这里登记。加新接口要来这里加一行 |
| 3 | `app/api/client/v1/auth.py` | 接口层 | 收到登录请求，校验参数，调用 service |
| 4 | `app/schemas/client/auth.py` | 短 | 规定请求和响应长什么样 |
| 5 | `app/services/client/auth.py` | 业务层 | 查用户、验密码、发令牌 |
| 6 | `app/models/user.py` | 38 | users 表的定义 |
| 7 | `app/core/security.py` | 短 | 生成和校验 JWT |
| 8 | `app/schemas/response.py` | 短 | 统一的返回格式 |

### 做新功能时照着抄的样板

阶段 1 做「目标」这个功能时，每一层都有现成的文件可以对照。

| 要新增的 | 照着哪个文件写 |
| --- | --- |
| `app/models/goal.py` | `app/models/user.py` |
| 迁移文件 | `migrations/versions/` 里现有的三个，用 `alembic revision --autogenerate` 生成 |
| `app/schemas/client/goal.py` | `app/schemas/client/auth.py` |
| `app/services/client/goal.py` | `app/services/client/auth.py` |
| `app/api/client/v1/goals.py` | `app/api/client/v1/demo.py` |
| 登记路由 | `app/route/router_registry.py` |
| 测试 | `tests/test_example.py` |

### 智能体会用到的现成零件

| 需要 | 脚手架里已有的 | 行数 | 还差什么 |
| --- | --- | --- | --- |
| 调用模型 | `app/services/client/ai_service.py` | 148 | 有对话、流式、结构化输出；没有工具调用，阶段 2 要加 |
| 流式推送给浏览器 | `app/api/client/v1/ai.py` 的 `chat_stream` | 84 | 是现成的 SSE 写法，阶段 2 照着写 goals 的 events 接口 |
| 后台任务 | `app/core/celery_app.py`、`app/schedule/jobs/demo.py` | 46、42 | demo 任务演示了 worker 里怎么连数据库，阶段 2 照着写智能体任务 |
| 定时触发 | `celery_app.py` 里的 `beat_schedule` | | 现在每分钟跑一次 demo，阶段 3 换成心跳 |
| Redis | `app/services/common/redis.py` | | 阶段 2 用它发布和订阅进度 |
| 发邮件 | `app/services/common/email*.py`、`resources/emails/` | | 阶段 3 用来发通知 |
| 容器编排 | `docker-compose.yml`、`.dev.yml`、`.prod.yml` | 154、68、73 | 生产配置已经关掉了容器内的 nginx，正好换成服务器上的 Caddy |
| 部署说明 | `部署文档.md`、`scripts/deploy.sh` | 166、111 | 阶段 1 参照；deploy.sh 里有旧项目名要清理 |

### 用户表里已经有求职相关的字段

`app/models/user.py` 里有 `career_goal`、`location`、`university`、`contract_types`。阶段 4 做记忆页时，求职偏好可以先复用它们，不够再加表。

### 已知的 4 个遗留问题（阶段 1 第一个任务）

| 位置 | 问题 | 影响 |
| --- | --- | --- |
| `app/utils/utils.py` 第 3、11、12 行 | 引用 `docx`、`PyPDF2`、`pandas`，`requirements.txt` 里没有 | 干净环境里应用启动即报错 |
| `app/utils/utils.py` 第 116 行 | `ALLOWED_AUDIO_TYPES` 未定义 | 走到那个分支会报错 |
| `app/exceptions/db_exceptions.py` 第 28 行 | 字符串内的引号没转义，语法错误 | 文件无法导入，目前没被引用所以没暴露 |
| `scripts/deploy.sh`、`resources/emails/auth/*.html` | 残留旧项目名 Prepwise，deploy.sh 还默认指向旧镜像地址 | 部署时会拉错镜像；邮件抬头不对 |

处理方向：`utils.py` 里真正被用到的只有 `get_temporary_credentials`（两个 aws 接口在用）。其余解析文件的函数是旧项目留下的，删掉比补依赖更干净。

## 对照组：FastAPI 官方全栈模板

下载在 `refs/fastapi-fullstack-template/`，是 FastAPI 作者本人维护的全栈模板。它不是用来照抄的，是用来回答「公认做得好的同类项目长什么样」。行数是 2026-10-07 核对的。

| 你要判断的 | 看它的哪个文件 | 行数 | 对应你的 |
| --- | --- | --- | --- |
| 一个「只能操作自己的东西」的增删改查怎么写 | `backend/app/api/routes/items.py` | 113 | 阶段 1 的 goals 接口 |
| 怎么拿到当前登录的用户 | `backend/app/api/deps.py` | 57 | `backend/app/api/client/deps.py` |
| 表和数据格式怎么定义 | `backend/app/models.py` | 126 | `app/models/`、`app/schemas/` |
| 接口测试怎么写 | `backend/tests/api/routes/test_items.py` | | `backend/tests/` |
| 登录页怎么写 | `frontend/src/routes/login.tsx` | 142 | 阶段 1 的登录页 |
| 前端目录怎么分 | `frontend/src/` 下的 routes、components、client、hooks | | `frontend/src/` |
| 上线说明怎么写 | `deployment-docker-compose.md` | 129 | `deploy/README.md`、`backend/部署文档.md` |
| CI 怎么写 | `.github/workflows/test-backend.yml` | 45 | `.github/workflows/ci.yml` |

它和本项目的差异：它把表和数据格式写在同一个文件里（用 SQLModel），你的脚手架分成 models 和 schemas 两层再加一层 services；它用 Traefik，本项目用 Caddy；它的前端用了更多的库。这些差异本身就是很好的审查题：哪种更适合一个要长期加功能的项目？

## 第二部分：参考项目

### 重要更正

nanobot 最新版已经不是「4000 行」了。当天实测，最新主分支的 Python 代码约 17 万行。真正适合通读的是它 2026 年 2 月的早期版本 `v0.1.3.post4`，共 4859 行。

所以 `scripts/fetch_refs` 下载的是这个早期版本，放在 `refs/nanobot-early/`。面试时的说法是「我读的是 nanobot 的早期版本，后来它也长大了」。

### 各项目怎么用

| 项目 | 下载到 | 用法 | 许可证 |
| --- | --- | --- | --- |
| nanobot 早期版本 | `refs/nanobot-early/` | 通读，照着结构自己写 | MIT |
| nanobot 最新版 | 不下载，需要时在 GitHub 上查 | 只查特定问题，见文末 | MIT |
| OpenClaw | 不下载 | 只读架构文档 https://clawdocs.org/architecture/overview | MIT |
| browser-use | 不下载 | 第一版不用。以后要操作网页时再当库引入 | 用前看一眼仓库 |
| GPT Researcher | `refs/gpt-researcher/`（可选） | 只看它的调研流程，写进技能文件 | 用前看一眼仓库 |

### 模块对照：refs/nanobot-early/nanobot/ 下的文件

| 本项目模块 | 对应文件 | 行数 | 看什么 |
| --- | --- | --- | --- |
| 网关：事件 | `bus/events.py` | 37 | 进来的消息和出去的消息长什么样。全项目最短，先读它 |
| 网关：队列 | `bus/queue.py` | 81 | 一个进队列、一个出队列，就是整个「总机」 |
| 网关：装配 | `cli/commands.py` | 656 | 只看 `gateway` 命令那一段：各个服务怎么被组装到一起启动 |
| 智能体循环 | `agent/loop.py` | 337 | 核心。看 `run` 和 `_process_message`：取消息、组上下文、调模型、执行工具、循环 |
| 模型接口 | `providers/base.py`、`providers/litellm_provider.py` | 69、173 | 怎么做到换模型不改循环 |
| 上下文组装 | `agent/context.py` | 217 | 系统提示词是哪几层拼起来的 |
| 工具 | `agent/tools/base.py`、`registry.py` | 102、73 | 一个工具的最小接口；工具怎么注册和查找 |
| 具体工具 | `agent/tools/web.py`、`filesystem.py`、`shell.py`、`message.py` | 163、191、141、86 | 挑 `web.py` 精读，其余扫一眼 |
| 技能 | `agent/skills.py` 和 `nanobot/skills/` 目录 | 228 | 技能文件怎么被发现、怎么按需加载进上下文 |
| 记忆 | `agent/memory.py` | 109 | Markdown 记忆最朴素的实现 |
| 会话 | `session/manager.py` | 202 | 对话历史怎么存盘、怎么读回 |
| 心跳 | `heartbeat/service.py` | 130 | 每 30 分钟发一句固定提示词；没事就回 `HEARTBEAT_OK` |
| 定时任务 | `cron/service.py`、`cron/types.py` | 346、59 | 定时任务怎么存、怎么触发 |
| 聊天入口 | `channels/base.py`、`manager.py`、`telegram.py` | 121、139、302 | 一个渠道要实现哪几个方法 |
| 子智能体 | `agent/subagent.py` | 240 | 先不做，知道有这回事即可 |

### 建议的阅读顺序

一共十个文件，约 1900 行。每读完一个，用一句话写下「它解决什么问题」。

1. `bus/events.py`
2. `bus/queue.py`
3. `agent/loop.py`
4. `agent/context.py`
5. `agent/tools/base.py` 和 `registry.py`
6. `agent/tools/web.py`
7. `heartbeat/service.py`
8. `session/manager.py`
9. `channels/telegram.py`
10. `cli/commands.py` 里的 `gateway` 命令

### 参考项目里没有、需要你自己设计的两块

这两块正是本项目和「又一个 nanobot」的区别，也是简历上最值得写的部分。

| 模块 | nanobot 早期版本的情况 | 你的设计依据 |
| --- | --- | --- |
| 任务与状态 | 只存对话历史，没有「目标、任务、步骤」的状态机，进程挂了不能续跑 | Muse 的目标页和持久状态；`docs/PRD.md` 的 F2；在本项目里落到 PostgreSQL 的 tasks、steps 表 |
| 权限与审批 | 没有独立的审批闸门 | Muse 的 Sentinel 文章；OpenClaw 的 Exec Approval Manager |

### 最新版 nanobot 里值得查的文件

只在对应阶段遇到问题时去 GitHub 上看，不通读。

| 想解决的问题 | 文件 |
| --- | --- |
| 断点恢复别人怎么做 | `nanobot/session/recovery.py`、`nanobot/session/goal_state.py` |
| 长任务怎么表达 | `nanobot/agent/tools/long_task.py` |
| 上下文超长怎么压缩 | `nanobot/agent/autocompact.py`、`nanobot/agent/context_governance.py` |
| 权限怎么管 | `nanobot/security/`、`nanobot/agent/goal_permission.py` |
| 飞书怎么接 | `nanobot/channels/feishu/` |

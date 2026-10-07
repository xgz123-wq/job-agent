# app/agent：智能体

这个目录现在是空的，阶段 2 开始往里写。它被 service 和 Celery 任务调用，自己不处理 HTTP。

## 文件约定

| 文件 | 做什么 | 阶段 | 参照 |
| --- | --- | --- | --- |
| `loop.py` | 智能体循环：模型想、调工具、看结果、再想。不超过 200 行 | 2 | `refs/nanobot-early/nanobot/agent/loop.py` |
| `judges.py` | 你亲手写的判断函数，全部放在这一个文件里 | 2 起 | 无 |
| `tools/base.py`、`tools/registry.py` | 工具的最小接口和注册表 | 2 | `refs/nanobot-early/nanobot/agent/tools/` |
| `tools/search.py`、`tools/fetch_url.py` | 两个只读工具 | 2 | `refs/nanobot-early/nanobot/agent/tools/web.py` |
| `skills/*.md` | 写给模型看的操作手册 | 2 起 | `refs/nanobot-early/nanobot/skills/` |
| `context.py` | 把身份、记忆、技能、历史拼成一次模型调用的上下文 | 2，阶段 4 加记忆 | `refs/nanobot-early/nanobot/agent/context.py` |
| `guard.py` | 审批闸门 | 4 | Muse 的 Sentinel 文章 |
| `memory.py` | 记忆的读写和压缩 | 4 | `refs/nanobot-early/nanobot/agent/memory.py` |

## 智能体用到、但不放在这个目录的东西

| 东西 | 在哪 | 为什么 |
| --- | --- | --- |
| goals、tasks、steps 等表 | `app/models/` | 表定义统一放 models |
| 状态机、目标的增查 | `app/services/client/` | 业务逻辑统一放 services |
| 跑智能体的后台任务 | `app/schedule/jobs/` | Celery 任务统一放这里 |
| 心跳的定时配置 | `app/core/celery_app.py` | beat 的配置在这里 |
| 接口 | `app/api/client/v1/` | 接口统一放 api |

## judges.py 里会有的函数

这些是架构判断，由你来写。每个十几行，教练提供签名和测试。

| 函数 | 回答什么问题 | 阶段 |
| --- | --- | --- |
| `should_stop` | 循环该不该停 | 2 |
| `has_sources` | 报告的结论是否都带来源 | 2 |
| `can_transition` | 这个状态转换合不合法 | 3 |
| `next_action_on_resume` | 重启后未完成的步骤怎么处理 | 3 |
| `should_notify` | 值不值得打扰用户 | 3 |
| `classify_action` | 这个动作属于哪一级 | 4 |
| `gate_decision` | 放行、拒绝还是问用户 | 4 |

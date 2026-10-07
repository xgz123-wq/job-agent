# job-agent

> 给面试官看的说明。阶段 5 会重写，现在是占位。

一个部署在自己服务器上的求职长程智能体，对标 Meta Muse。用户在网页上给它一个目标，它在后台拆步骤、持续执行、实时汇报进度，不可撤销的操作要用户在网页上批准。

## 技术栈

| 层 | 技术 |
| --- | --- |
| 前端 | React + TypeScript + Vite + Tailwind |
| 后端 | FastAPI（异步）、SQLAlchemy、Alembic |
| 数据 | PostgreSQL、Redis |
| 后台任务 | Celery worker + beat |
| 智能体 | 自研循环，参照 OpenClaw 与 nanobot 早期版本 |
| 部署 | Docker Compose、Caddy（自动 HTTPS）、GitHub Actions |

## 文档

- 架构：`docs/ARCHITECTURE.md`
- 设计决策：`docs/DECISIONS.md`
- 进度：`coach/PROGRESS.md`

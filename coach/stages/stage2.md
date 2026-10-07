# 阶段 2：智能体最小闭环

**你的角色**：Agent 工程师。

**目标**：F1 公司调研。在网页上新建一个调研目标，后台的智能体自己搜索、读网页、汇总；网页实时显示每一步；最后出一页带来源的报告。

**完成后简历上可以写**：实现了基于工具调用的智能体循环，运行在 Celery worker 中，步骤持久化到 PostgreSQL，并通过 Redis 发布订阅与 SSE 将执行过程实时推送到前端。

## 先学再做：建立你的判断标准

动手之前先花约 2.5 小时。资料和「只看哪几节」在 `docs/RESOURCES.md` 的 H2。

1. **看**：带 ★ 的必看，其余选看。
2. **写**：把你的标准写进 `coach/standards/agent.md`，五条以内，每条配一个反例。
3. **对照**：读 `refs/nanobot-early/nanobot/agent/loop.py`，用你的标准给它打分。它哪里做得好，哪里你会改？
4. **审查**：教练做完后说「审查」，用你的标准逐条检查它的产出。


## 先读

- `refs/nanobot-early/nanobot/agent/loop.py`、`agent/tools/base.py`、`registry.py`、`web.py`
- `backend/app/services/client/ai_service.py`、`app/api/client/v1/ai.py`、`app/schedule/jobs/demo.py`
- `backend/app/agent/README.md`

## 你要写的设计说明

`coach/designs/stage2-loop.md`：

1. 循环什么时候算完成？列出所有会让它停下的情况。
2. 最多跑几步、最多花多少钱？超了是直接停，还是交一份半成品？
3. 工具报错后循环怎么处理？
4. 「公司调研」哪些做成工具，哪些写进技能文件？
5. steps 表每一行记什么？
6. 从 worker 到浏览器，一条进度消息经过哪几站？浏览器中途断开再连上，怎么补上错过的步骤？

## 教练要做

1. 给 `ai_service` 加工具调用能力。
2. `app/agent/loop.py`：不超过 200 行，参照 nanobot 早期版本。
3. `app/agent/tools/`：`search`、`fetch_url`。
4. tasks、steps 两张表和迁移。
5. Celery 任务：取目标，跑循环，每一步写 steps 并往 Redis 发布。
6. `GET /goals/{id}/events`：订阅 Redis，用 SSE 推送。
7. 前端目标详情页：计划、实时步骤、报告。
8. 技能文件 `app/agent/skills/company-research.md` 初稿，你来改。
9. 上线这一版。

## 你亲手写的判断函数

- `should_stop(state) -> tuple[bool, str]`：根据步数、花费、最近几步，判断该不该停并给出原因。
- `has_sources(report: str) -> bool`：检查报告的结论是否都带来源链接。

## 新概念

Redis、消息队列、Celery worker、SSE、工具调用。

## 验收

1. 线上新建调研目标，详情页不刷新就能看到步骤一条条出现。
2. 换 3 家公司都能跑完，报告的每条结论带来源链接。
3. 新建目标的接口在 1 秒内返回，不等智能体跑完。
4. 关掉浏览器再打开，任务仍在继续，已有的步骤都能看到。
5. 给一个不存在的公司名，它能在步数上限内停下并说明没查到。

另外：本阶段的标准文件已写好，并且做过至少一次「审查」和一次「二选一」，结论记在 PR 里。

## 搞坏实验

- 把最大步数改成 3，看它交出什么。
- 停掉 worker 容器再新建目标，观察目标停在什么状态；启动 worker 后又发生什么。
- 停掉 Redis，看接口和 worker 各自报什么错。
- 把搜索工具改成永远返回空，看它会不会绕圈子。

## 口述检查题

1. 从点击「开始」到看到第一条步骤，经过了哪些东西？
2. 模型是怎么「调用工具」的？
3. 为什么新建目标的接口能马上返回？
4. 进度为什么经过 Redis，而不是 worker 直接推给浏览器？
5. 你的终止条件有哪几条？
6. steps 表除了给页面显示，还有什么用？

## 预想卡点

| 卡点 | 对策 |
| --- | --- |
| 分不清接口进程和 worker 进程 | 它们是两个容器，代码相同，启动命令不同。让教练带你看 compose 文件 |
| worker 里用不了接口里的数据库会话 | 照 demo 任务的写法 |
| 线上 SSE 攒成一坨才出来 | 反向代理缓冲。见 `docs/PITFALLS.md` |
| 模型不按格式调用工具 | 检查工具的描述和参数定义。记进卡点记录，这是好的面试素材 |
| 报告质量差 | 先查 steps 表定位是哪一步的问题 |

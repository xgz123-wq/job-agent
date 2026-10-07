# 学习资料与判断标准

这份清单解决一个问题：AI 帮你做出来了，你怎么判断它做得好不好。

做法是每个阶段动手之前，先看少量由真正做过的人写的资料，只看指定的几节，然后写下你自己的标准，最后用这套标准去审查教练的产出。

## 怎么用

每个钩子都是同样的四步，时间控制在标注的范围内，超了就停：

1. **看**：先看带 ★ 的，其余选看。只看「只看这些」一栏写的部分。
2. **写**：在 `coach/standards/` 里写下你的标准，五条以内，每条配一个反例。模板在 `coach/standards/TEMPLATE.md`。
3. **对照**：打开「对照组」，那是公认做得好的同类实现。找一处符合你标准的地方，一处和你的项目不同的地方。
4. **审查**：教练做完后说「审查」，用你的标准逐条检查。

英文资料有三种读法：浏览器整页翻译；视频开自动翻译字幕；让教练带读，它讲一段你复述一段。教练可以带读，不能替你写标准。

## 关于这份清单的可靠程度

- 选择依据是作者身份和公开的目录，不是我看完之后的评价。视频我没有逐个看过。
- 「核实」一栏：✓ 表示 2026-10-07 打开过页面或仓库确认存在且内容对得上；○ 表示是长期稳定的官方地址，这次没有逐个打开。
- 视频不给时间戳，按章节标题在视频的章节列表里找。
- 有的资料年份较早（标注了），讲的是不变的基本功，具体工具可能和本项目不同，差异已写明。
- 链接失效或内容对不上时，告诉教练，让它找替代并更新这张表。

## 对照组：贯穿全程的参照物

| 参照物 | 是什么 | 用来对照什么 | 核实 |
| --- | --- | --- | --- |
| [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | FastAPI 作者本人维护的官方全栈模板：FastAPI、React、TypeScript、PostgreSQL、Docker Compose、GitHub Actions。已下载到 `refs/fastapi-fullstack-template/` | 后端结构、前端结构、测试、部署文档、CI | ✓ |
| `refs/nanobot-early/` | nanobot 的早期版本，约 4900 行 | 智能体循环、工具、心跳 | ✓ |
| Muse 本身和它的两篇官方文章 | 你用过的成品 | 产品设计、审批、安全 | ✓ |

对照组和本项目的选型不完全一样。官方模板用 SQLModel、Traefik 和一套组件库，本项目用 SQLAlchemy、Caddy 和 Tailwind。对照的是思路和组织方式，不照抄。

---

## H0 产品与原型（阶段 0，约 2 小时）

写入 `coach/standards/product.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R01 | [How We Designed Muse](https://introducing.muse.ai) | 文章，英文，15 分钟 | Muse 的产品和设计负责人 | 全文。重点是 Getting Things Done With Muse 一节的四个小标题 | ✓ |
| ★ R02 | [Muse 产品演示](https://www.youtube.com/watch?v=wHn0hTjvFoo) | 视频，英文 | Muse 产品设计负责人，上面那篇文章里给的链接 | 目标页、活动日志、审批卡片出现的片段，各截一张图 | ○ |
| R03 | [尼尔森十大可用性原则](https://www.nngroup.com/articles/ten-usability-heuristics/) | 文章，英文，中文译文很多 | Jakob Nielsen，界面评审的通用标准 | 第 1 条系统状态可见、第 3 条用户可控、第 5 条防错、第 9 条帮用户从错误中恢复 | ○ |
| R04 | [Shape Up](https://basecamp.com/shapeup) | 在线书，英文，免费 | Basecamp 的产品负责人 Ryan Singer | 只看 Find the Elements 一章：先画流程和要素，不先画好看的界面 | ○ |

对照组：Muse 本身。

看完要能回答：

1. 一个长时间在后台干活的产品，界面上必须让用户随时看到哪三样东西？
2. 为什么审批要做成独立的卡片，而不是让智能体在对话里问一句？
3. 原型阶段先确定什么、后确定什么？什么东西现在不该花时间？
4. 拿尼尔森那四条去看 `docs/PROTOTYPE.md` 的五个页面，哪一页最不达标？

---

## H1a 协作规范（阶段 1 任务 1 之前，约 30 分钟）

写入 `coach/standards/workflow.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R14 | [GitHub 流程](https://docs.github.com/zh/get-started/using-github/github-flow) | 文档，中文，10 分钟 | GitHub 官方 | 全文 | ○ |
| ★ R15 | [约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/) | 文档，中文，10 分钟 | 社区规范 | 「概述」和「示例」 | ○ |
| R05 | [Python API Development](https://youtu.be/0sOvCWFmrtA)（[目录](https://www.freecodecamp.org/news/creating-apis-with-python-free-19-hour-course/)） | 视频，英文，2021 年 | Sanjeev Thiyagarajan，freeCodeCamp 发布 | 第 17 部分 CI/CD pipeline 的前三节：CI/CD intro、Github Actions、Creating Jobs | ✓ |

对照组：`refs/fastapi-fullstack-template/.github/workflows/test-backend.yml`（45 行）。

看完要能回答：

1. 一条好的提交信息和一条差的，各举一个例子。
2. 只有一个人的项目，为什么还要开 PR？
3. CI 应该在什么时候跑？红了之后正确的做法是什么？

---

## H1b 后端与数据（阶段 1 任务 2 之前，约 2.5 小时）

写入 `coach/standards/backend.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R05 | [Python API Development](https://youtu.be/0sOvCWFmrtA) | 视频，英文，2021 年 | 同上。他从零做了一个带登录、数据库、测试、部署的完整接口项目 | 第 6 部分 ORM intro；第 7 部分 Pydantic vs ORM Models；第 8 部分从 JWT Token Basics 到 Protecting Routes；第 9 部分 Delete and Update only your own posts 和 Environment Variables；第 11 部分前三节讲迁移 | ✓ |
| ★ R07 | [RESTful API 最佳实践](https://www.ruanyifeng.com/blog/2018/10/restful-api-best-practices.html) | 文章，中文，10 分钟，2018 年 | 阮一峰 | 全文。讲地址怎么起名、用哪个动词、返回什么状态码 | ○ |
| R06 | [FastAPI 官方教程](https://fastapi.tiangolo.com/zh/tutorial/) | 文档，中文 | FastAPI 作者 | 「更大的应用 - 多个文件」「安全性」一组里讲 JWT 的那页 | ✓ |
| R08 | [十二要素应用](https://12factor.net/zh_cn/) | 文档，中文 | Heroku 的工程师总结的线上应用规范 | 第 3 条配置、第 10 条开发与线上环境等价、第 11 条日志 | ○ |

对照组：`refs/fastapi-fullstack-template/backend/app/api/routes/items.py`（113 行）。它是一个「只能操作自己的东西」的增删改查，和你要做的 goals 是同一类。再看 `backend/app/api/deps.py`（57 行）怎么拿到当前用户，`backend/tests/api/routes/test_items.py` 怎么测。

看完要能回答：

1. 一个好的接口地址长什么样？`/getGoalList` 差在哪？
2. 请求的数据格式定义和数据库表定义为什么要分成两个类？
3. 「只能看自己的目标」这条规则，官方模板写在哪一层？你的脚手架应该写在哪一层？
4. 密钥为什么不能写在代码里？官方模板和你的脚手架各是怎么读配置的？
5. 一个接口至少要测哪两种情况？

---

## H1c 前端（阶段 1 任务 3 之前，约 3 小时）

写入 `coach/standards/frontend.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R09 | [教程：井字棋游戏](https://zh-hans.react.dev/learn/tutorial-tic-tac-toe) | 交互式教程，中文，1.5 小时 | React 官方 | 做到「完成游戏」一节结束。「时间旅行」可以不做 | ✓ |
| ★ R09b | [React 哲学](https://zh-hans.react.dev/learn/thinking-in-react) | 文档，中文，20 分钟 | React 官方 | 全文。讲怎么把一张设计图拆成组件、状态放在哪 | ○ |
| R10 | [Refactoring UI 专栏](https://medium.com/refactoring-ui) 里的 7 Practical Tips for Cheating at Design | 文章，英文，10 分钟 | Adam Wathan 和 Steve Schoger，Tailwind 的作者和设计师 | 全文，主要看配图 | ○ |
| R03 | 尼尔森十大可用性原则 | 见 H0 | | 用来审查做出来的页面 | ○ |

对照组：`refs/fastapi-fullstack-template/frontend/src/routes/login.tsx`（142 行）和 `frontend/src/` 的目录分法。它用的路由和组件库比本项目复杂，只看三件事：页面、组件、请求封装各放在哪。

看完要能回答：

1. 按 React 哲学的五步，把目标列表页拆成哪几个组件？
2. 一份数据应该放在哪个组件里，判断依据是什么？
3. 页面正在加载、请求失败、列表为空，这三种状态各显示什么？缺了哪种算不合格？
4. 发请求的代码散落在各个页面里，和集中在一处，哪种好？为什么？
5. 不懂设计的人让界面看起来不乱，最省事的两三个办法是什么？

---

## H1d 部署（阶段 1 任务 4 之前，约 2 小时）

写入 `coach/standards/deploy.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R11 | [Docker 1 小时快速上手教程](https://www.bilibili.com/video/BV11L411g7U1/) | 视频，中文，共 8 节 | B 站教程，每节十分钟以内 | 第 1 节简介和安装、第 3 节构建自己的镜像、第 5 节多容器通信、第 6 节 docker-compose，共约 35 分钟 | ✓ |
| ★ R12 | FastAPI 文档的[关于 HTTPS](https://fastapi.tiangolo.com/zh/deployment/https/)和[部署概念](https://fastapi.tiangolo.com/zh/deployment/concepts/) | 文档，中文，30 分钟 | FastAPI 作者 | 两页全文。前一页用图讲清域名、证书、代理的关系，后一页列出部署要考虑的六件事 | ✓ |
| R05 | [Python API Development](https://youtu.be/0sOvCWFmrtA) | 视频，英文 | 同上 | 第 14 部分的 Setting up Domain name、SSL/HTTPS、Firewall、Pushing code changes to Production；第 15 部分的 Production vs Development。他用 Nginx，本项目用 Caddy，概念相同 | ✓ |
| R13 | [Caddy 反向代理快速上手](https://caddyserver.com/docs/quick-starts/reverse-proxy) | 文档，英文，5 分钟 | Caddy 官方 | 全文 | ○ |

对照组：`refs/fastapi-fullstack-template/deployment-docker-compose.md`（129 行）和你脚手架的 `backend/部署文档.md`。两份都是真实的上线说明，对比它们的章节顺序。

看完要能回答：

1. 镜像和容器是什么关系？
2. 浏览器访问你的域名，到请求进入接口容器，中间经过哪几站？
3. 「部署概念」那页列的六件事，本项目各由谁负责？
4. 哪些端口该对公网开放，哪些绝对不该？
5. 一份合格的上线说明应该包含哪几部分？

---

## H2 智能体循环与工具（阶段 2 之前，约 2.5 小时）

写入 `coach/standards/agent.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R18 | [《深入理解 AI Agent》](https://github.com/bojieli/ai-agent-book) | 开源书，中文 | 李博杰。你已经在读 | 讲 Agent 基础的一章和讲工具的一章。章号以仓库目录为准 | ✓ |
| ★ R16 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 文章，英文，20 分钟 | Anthropic 的工程团队，总结他们和几十个团队合作的经验 | When (and when not) to use agents；Agents 小节；附录 2 讲怎么给工具写说明 | ✓ |
| R17 | [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 文章，英文 | Anthropic 工程团队 | 讲工具命名、参数、返回内容的原则部分 | ✓ |
| R19 | [12-Factor Agents](https://ai.engineer/talks/12-factor-agents) | 视频，英文，17 分钟，页面带文字稿 | Dex Horthy，HumanLayer 创始人 | JSON & Tools 和 Control Flow 两段 | ✓ |
| R20 | [Celery 入门](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)和 [MDN 的 SSE 用法](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events/Using_server-sent_events) | 文档 | 官方 | Celery 只看 Application 和 Calling the task 两节；SSE 看到「事件流格式」为止 | ○ |

对照组：`refs/nanobot-early/nanobot/agent/loop.py`（337 行）和 `agent/tools/base.py`（102 行）。

看完要能回答：

1. 什么情况下根本不该用智能体，一次模型调用或固定流程就够了？公司调研属于哪种？
2. 一个好的工具说明应该写清哪几样？拿你的 `search` 工具举例。
3. 循环的控制权在谁手里：模型说停就停，还是代码说了算？各有什么风险？
4. 工具报错时，把什么信息还给模型才有用？
5. 对照 nanobot 的 loop.py，它的终止条件有哪些？你的多了什么、少了什么？

---

## H3 长程与可靠性（阶段 3 之前，约 2 小时）

写入 `coach/standards/reliability.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R19 | [12-Factor Agents](https://ai.engineer/talks/12-factor-agents) 和它的[仓库](https://github.com/humanlayer/12-factor-agents) | 视频加文档，英文 | Dex Horthy。他的公司做的就是让智能体暂停等人批准 | 视频的 Pause & Resume 和 Stateless Agents 两段；仓库里的第 5、6、12 条 | ✓ |
| ★ R21 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 文章，英文 | Anthropic 工程团队 | 讲智能体怎样跨多次会话接着干、靠什么文件记住进度的部分 | ✓ |
| R01 | How We Designed Muse | 见 H0 | | Muse Is an Agent That Can Actually Do Things 一节的最后一段：后台工作做完后怎么决定通不通知 | ✓ |

对照组：最新版 nanobot 的 `nanobot/session/recovery.py`（在 GitHub 上看）；Muse 的目标页。

看完要能回答：

1. 「执行状态」和「业务状态」分开存会出什么问题？你的 steps 表属于哪种？
2. 一个能暂停和恢复的智能体，暂停时必须存下什么？
3. 「无状态」是什么意思？为什么它让断点恢复变简单？
4. 哪类步骤重做一遍没关系，哪类绝对不能重做？你怎么区分？
5. 一条通知值不值得发，你的判断标准是什么？

---

## H4 安全与记忆（阶段 4 之前，约 2.5 小时）

写入 `coach/standards/safety.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R22 | [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 文章，英文 | Muse 的工程负责人 | A Built-In Sentinel、Human in the Loop、Least Privilege、Defense in Depth 四节 | ✓ |
| ★ R23 | [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | 文章，英文，10 分钟 | Simon Willison，「提示词注入」这个词的提出者 | 全文 | ✓ |
| R24 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 文章，英文 | Anthropic 工程团队 | The anatomy of effective context；讲长任务里压缩和记笔记的部分 | ✓ |
| R18 | 《深入理解 AI Agent》 | 书，中文 | 李博杰 | 讲上下文的一章和讲记忆的一章 | ✓ |
| R19 | 12-Factor Agents | 见 H2 | | Human Contact 一段和仓库第 7 条 | ✓ |

对照组：Muse 的审批卡片（你的截图）；OpenClaw 架构文档里的 Prompt Assembly 表。

看完要能回答：

1. 「致命三要素」是哪三样？你的智能体占了几样？去掉哪一样最容易？
2. 为什么审批必须由循环之外的代码裁决？
3. 「最小权限」在你的项目里体现在哪两个地方？
4. Muse 说它不想让用户对弹窗麻木。它的默认策略是什么？你的呢？
5. 上下文里哪些内容每次都带，哪些按需取，哪些该压缩？

---

## H5 评测（阶段 5 之前，约 2 小时）

写入 `coach/standards/evals.md`。

| 编号 | 资料 | 形式 | 谁做的 | 只看这些 | 核实 |
| --- | --- | --- | --- | --- | --- |
| ★ R25 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 文章，英文 | Anthropic 工程团队 | 讲评分方式有哪几类、从零搭评测分几步的部分 | ✓ |
| ★ R18 | 《深入理解 AI Agent》 | 书，中文 | 李博杰 | 讲评估的一章，只看方法，不做里面的基准实验 | ✓ |
| R26 | [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) | 文章，英文 | Hamel Husain，帮多家公司搭过评测 | 讲三个层次的评测和「先看数据」的部分 | ○ |

对照组：你自己两轮评测的数字。

看完要能回答：

1. 评分有哪几种方式？你的 15 个任务各用哪种？
2. 为什么要先人工看一批真实的执行记录，再写自动评分？
3. 一个指标从 60% 变成 70%，怎样才算真的进步而不是碰巧？
4. 评测集太容易或太难，各有什么表现？

---

## 以后想深入时再看

现在不要看。做完阶段 5 之后按兴趣选。

- freeCodeCamp 那门课的第 16 部分：系统地学 pytest。
- 《深入理解 AI Agent》的多 Agent 协作一章。
- 12-Factor Agents 仓库的其余各条。
- 官方全栈模板的前端测试和自动部署流水线。

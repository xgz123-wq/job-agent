# 从这里开始

这是一个完整的全栈项目仓库的起点：一个部署在自己服务器上的求职长程智能体。你会把从产品定位、原型、后端、前端、智能体到上线的整条链路走一遍。

## 仓库里现在有什么

| 目录 | 内容 | 状态 |
| --- | --- | --- |
| `backend/` | 你的 fastapi-scaffold（复制自提交 ff04d77） | 能用，但有 4 个遗留问题，见下 |
| `frontend/` | 前端 | 空，阶段 1 创建 |
| `deploy/` | 上线清单和反向代理配置示例 | 阶段 1 使用 |
| `docs/` | PRD、架构、概念卡、原型、规范、面试清单 | 已写好 |
| `coach/` | 教练的任务书、进度、你的学习档案 | 已写好 |
| `coach/standards/` | 你自己写的判断标准 | 空，由你来写 |
| `docs/RESOURCES.md` | 每个阶段看什么资料、只看哪几节 | 已写好 |
| `CLAUDE.md` | 给 Claude Code 的教练规则 | 已写好 |
| `.github/` | CI 流水线和 PR 模板 | 已写好，第一次推送后会是红的，见下 |

## 今天要做的事

1. 解压，进入文件夹，初始化仓库并推到 GitHub：

   ```bash
   git init
   git add .
   git commit -m "chore: 项目起步包"
   git branch -M main
   git remote add origin <你新建的 GitHub 仓库地址>
   git push -u origin main
   ```

2. 运行 `python scripts/check_env.py`，看缺什么。
3. 运行 `bash scripts/fetch_refs.sh`（Windows 用 `scripts/fetch_refs.ps1`），下载参考项目到 `refs/`。
4. 在这个文件夹里启动 Claude Code，输入：`开始`。它会带你进入阶段 0。

## 先知道两件事

**第一，CI 第一次会是红的，这是预期的。** 我在干净环境里实测了你的脚手架，发现 4 个遗留问题：

1. `backend/app/utils/utils.py` 引用了 `docx`、`PyPDF2`、`pandas`，但它们已经从 `requirements.txt` 里删掉了。结果是在干净环境里应用启动就会报错。
2. 同一个文件第 116 行用了没定义的 `ALLOWED_AUDIO_TYPES`。
3. `backend/app/exceptions/db_exceptions.py` 第 28 行有语法错误（字符串里的引号没转义）。目前没有别处引用它，所以没暴露。
4. `backend/scripts/deploy.sh` 和三个邮件模板里还留着旧项目的名字 Prepwise。

把它们修好、让 CI 变绿，是阶段 1 的第一个任务。它正好能让你体会「我本地能跑」和「干净环境能跑」的区别，这是企业开发里最基本的一课。

**第二，仓库就是记忆。** 网页端的 Claude 和本地的 Claude Code 互相看不到对方的对话。两边共享的只有这个仓库里的文件：进度在 `coach/PROGRESS.md`，你学会了什么在 `coach/LEARNER.md`，做过的决定在 `docs/DECISIONS.md`。每次收工都提交并推送。回到网页端时，把仓库地址或 `coach/PROGRESS.md` 的内容发过来即可接上。

## 七个口令

| 口令 | 它会做什么 |
| --- | --- |
| `开始` | 读进度，告诉你今天做哪一步 |
| `这是什么 X` | 用一张概念卡讲清 X：是什么、在本项目里干什么、学到哪就够 |
| `卡住了` | 问清三件事，分清类型，再对症处理 |
| `审查` | 你用自己写的标准，逐条检查它的产出 |
| `讲一遍` | 你口述，它扮面试官追问 |
| `验收` | 按当前阶段的标准逐条实际检查 |
| `收工` | 更新进度和学习档案，提交并推送 |

## 每个阶段的节奏：学、定标准、做、审查

这个项目不是让 AI 替你做完。每个阶段动手之前，你先看少量指定的资料（文章和视频都有，只看指定的几节），在 `coach/standards/` 写下你自己的「好的标准」，然后教练才开始写代码。它写完后，你用自己的标准审查它。

资料清单在 `docs/RESOURCES.md`，一共九个钩子，每个 30 分钟到 3 小时。

## 一条原则

每样技术只学到够用的 20%：知道它是什么、在这个项目里负责什么、出了问题去哪看。标准写在 `docs/CONCEPTS.md`。剩下的用到再学。

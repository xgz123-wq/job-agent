# frontend

现在是空的。阶段 1 的任务 3 由教练在这里创建 React + TypeScript + Vite + Tailwind 项目。

页面设计见 `docs/PROTOTYPE.md`。计划的结构：

```
frontend/
  src/
    pages/        登录、目标列表、目标详情、审批、记忆
    components/   可复用的小块
    api/          发请求的封装，统一带令牌
  index.html
  vite.config.ts  开发时把 /api 代理到后端
```

打包后的产物在 `frontend/dist/`，是一堆静态文件。上线时由 Caddy 直接提供。

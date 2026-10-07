"""环境自检。运行：python scripts/check_env.py"""
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
results = []


def check(name, ok, hint="", required=True):
    results.append((name, ok, hint, required))


def run(*cmd):
    try:
        out = subprocess.run(list(cmd), capture_output=True, text=True, timeout=20, cwd=ROOT)
        return out.returncode == 0, (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr).strip() else ""
    except Exception:
        return False, ""


check(
    f"Python 版本 {sys.version_info.major}.{sys.version_info.minor}",
    sys.version_info >= (3, 11),
    "需要 3.11 或更高（脚手架的镜像用 3.12）",
)

ok, ver = run("git", "--version")
check(f"git 已安装（{ver}）" if ok else "git 已安装", ok, "安装 git")

ok, ver = run("docker", "--version")
check(f"Docker 已安装（{ver}）" if ok else "Docker 已安装", ok, "阶段 1 之前装好 Docker Desktop 或 Docker Engine。到时对教练说「卡住了，没装 Docker」", required=False)

ok, ver = run("docker", "compose", "version")
check("Docker Compose 可用", ok, "新版 Docker 自带。命令是 docker compose，中间是空格", required=False)

ok, _ = run("docker", "info")
check("Docker 正在运行", ok, "启动 Docker 后再试", required=False)

ok, ver = run("node", "--version")
check(f"Node.js 已安装（{ver}）" if ok else "Node.js 已安装", ok, "阶段 1 做前端时才需要", required=False)

check("Claude Code 命令行可用", bool(shutil.which("claude")), "确认在终端里能运行 claude", required=False)

check("已初始化 git 仓库", (ROOT / ".git").exists(), "在项目根目录运行 git init", required=False)

ok, remote = run("git", "remote", "get-url", "origin")
check("已关联远程仓库", ok, "在 GitHub 新建仓库后运行 git remote add origin <地址>", required=False)

check(
    "已下载参考项目 refs/nanobot-early",
    (ROOT / "refs" / "nanobot-early" / "nanobot" / "agent" / "loop.py").exists(),
    "运行 bash scripts/fetch_refs.sh（Windows 用 scripts/fetch_refs.ps1）",
    required=False,
)

check(
    "已下载对照组 refs/fastapi-fullstack-template",
    (ROOT / "refs" / "fastapi-fullstack-template" / "backend" / "app" / "api" / "routes" / "items.py").exists(),
    "运行 bash scripts/fetch_refs.sh（Windows 用 scripts/fetch_refs.ps1）",
    required=False,
)

check("已创建 backend/.env", (ROOT / "backend" / ".env").exists(), "阶段 1 任务 1 时把 backend/.env.example 复制成 backend/.env", required=False)

print()
bad = 0
for name, ok, hint, required in results:
    mark = "通过" if ok else ("必须解决" if required else "待办")
    print(f"[{mark}] {name}")
    if not ok:
        print(f"        {hint}")
        bad += required
print()
if bad:
    print(f"有 {bad} 项必须先解决。")
    sys.exit(1)
print("必需项都通过了。下一步：在这个文件夹里启动 Claude Code，输入「开始」。")

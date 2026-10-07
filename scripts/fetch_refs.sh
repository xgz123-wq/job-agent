#!/usr/bin/env bash
# 下载参考项目到 refs/（只读，不进仓库）。加参数 all 会多下载 GPT Researcher。
set -e
cd "$(dirname "$0")/.."
mkdir -p refs

get() { # 名字 地址 [分支或标签]
  if [ -d "refs/$1" ]; then echo "已存在，跳过：$1"; return; fi
  echo "下载：$1"
  if [ -n "$3" ]; then git clone --depth 1 --branch "$3" "$2" "refs/$1"; else git clone --depth 1 "$2" "refs/$1"; fi
}

# nanobot 早期版本，约 4900 行，用来通读
get nanobot-early https://github.com/HKUDS/nanobot.git v0.1.3.post4

# FastAPI 作者的官方全栈模板，作为「好的做法」的对照组
get fastapi-fullstack-template https://github.com/fastapi/full-stack-fastapi-template.git

if [ "$1" = "all" ]; then
  get gpt-researcher https://github.com/assafelovic/gpt-researcher.git
fi

echo "完成。阅读顺序见 docs/REFERENCE_MAP.md"

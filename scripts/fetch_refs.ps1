# 下载参考项目到 refs/（只读，不进仓库）。加 -All 会多下载 GPT Researcher。
# 运行：powershell -ExecutionPolicy Bypass -File scripts/fetch_refs.ps1
param([switch]$All)

$root = Split-Path -Parent $PSScriptRoot
$refs = Join-Path $root "refs"
New-Item -ItemType Directory -Force -Path $refs | Out-Null

function Get-Ref($name, $url, $branch) {
    $dest = Join-Path $refs $name
    if (Test-Path $dest) { Write-Host "已存在，跳过：$name"; return }
    Write-Host "下载：$name"
    if ($branch) { git clone --depth 1 --branch $branch $url $dest }
    else { git clone --depth 1 $url $dest }
    if ($LASTEXITCODE -ne 0) { Write-Host "下载失败：$name。对教练说「卡住了」并贴上面的报错。" }
}

# nanobot 早期版本，约 4900 行，用来通读
Get-Ref "nanobot-early" "https://github.com/HKUDS/nanobot.git" "v0.1.3.post4"

# FastAPI 作者的官方全栈模板，作为「好的做法」的对照组
Get-Ref "fastapi-fullstack-template" "https://github.com/fastapi/full-stack-fastapi-template.git" $null

if ($All) {
    Get-Ref "gpt-researcher" "https://github.com/assafelovic/gpt-researcher.git" $null
}

Write-Host "完成。阅读顺序见 docs/REFERENCE_MAP.md"

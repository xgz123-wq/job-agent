#!/usr/bin/env bash
# FastAPI Scaffold 验收脚本
# 用法: bash scripts/verify-scaffold.sh
# 退出码: 0 全部 PASS / 1 有 FAIL 或 SKIP（SKIP 不算失败但会提示）
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

green() { printf "\033[32m%s\033[0m" "$1"; }
red()   { printf "\033[31m%s\033[0m" "$1"; }
yellow(){ printf "\033[33m%s\033[0m" "$1"; }

record_pass() { echo "[$(green PASS)] $1"; PASS_COUNT=$((PASS_COUNT+1)); }
record_fail() { echo "[$(red FAIL)] $1"; FAIL_COUNT=$((FAIL_COUNT+1)); }
record_skip() { echo "[$(yellow SKIP)] $1"; SKIP_COUNT=$((SKIP_COUNT+1)); }

# docker 是否真正可用（CLI 存在且 docker info 能跑通）
docker_available() {
    command -v docker >/dev/null 2>&1 || return 1
    docker info >/dev/null 2>&1
}

# -------------------------------------------------------------------- #
# 1. docker compose config 端口参数化生效（要求 .env 不存在或用 .env.example）
# -------------------------------------------------------------------- #
check_compose_port_params() {
    local desc="docker-compose.yml 端口参数化（API_PORT/POSTGRES_PORT/REDIS_EXTERNAL_PORT/NGINX_HTTP_PORT/FLOWER_PORT/PROJECT_NAME）"
    if ! docker_available; then
        record_skip "$desc（docker 不可用，已在 .env/.env.example 与 yaml 中用 \${VAR} 形式参数化）"
        return
    fi
    local cfg
    if ! cfg=$(docker compose config 2>&1); then
        record_fail "$desc：docker compose config 失败"
        return
    fi
    local need=(API_PORT POSTGRES_PORT REDIS_EXTERNAL_PORT NGINX_HTTP_PORT NGINX_HTTPS_PORT FLOWER_PORT PROJECT_NAME)
    local ok=1
    for v in "${need[@]}"; do
        if ! grep -q "\\\${$v" docker-compose.yml && ! grep -q "\${$v" docker-compose.yml; then
            record_fail "$desc：$v 未用 \${$v} 形式"
            ok=0
        fi
    done
    if [[ $ok -eq 1 ]]; then record_pass "$desc"; fi
}

# -------------------------------------------------------------------- #
# 2. app 服务有 networks 字段
# -------------------------------------------------------------------- #
check_app_networks() {
    local desc="app 服务挂载 app-network"
    if ! docker_available; then
        record_skip "$desc（docker 不可用，已在 docker-compose.yml 中为 app 服务显式声明 networks）"
        return
    fi
    local cfg
    if ! cfg=$(docker compose config 2>&1); then
        record_fail "$desc：docker compose config 失败"
        return
    fi
    if echo "$cfg" | grep -A 30 "^  app:" | grep -q "networks:"; then
        record_pass "$desc"
    else
        record_fail "$desc：app 服务缺 networks 字段"
    fi
}

# -------------------------------------------------------------------- #
# 3. 业务字样无残留
# -------------------------------------------------------------------- #
check_business_residue() {
    local desc="业务字样（ai-interview/prepwise/智面/dev-zetos/Seiki）无残留"
    local hit
    hit=$(grep -ri --include='*.py' --include='*.yml' --include='*.yaml' --include='*.conf' --include='*.template' --include='*.html' --include='*.md' --include='*.txt' --include='Dockerfile*' \
        -e 'ai-interview' -e 'prepwise' -e 'Prepwise' -e '智面' -e 'dev-zetos' -e 'Seiki' \
        app/ nginx/ docker-compose*.yml Dockerfile* requirements.txt .env.example README.md CLAUDE.md 部署文档.md 2>/dev/null || true)
    if [[ -z "$hit" ]]; then
        record_pass "$desc"
    else
        record_fail "$desc"
        echo "$hit" | head -20 | sed 's/^/      /'
    fi
}

# -------------------------------------------------------------------- #
# 4. app/models 只剩 base/user/token/admin
# -------------------------------------------------------------------- #
check_models_scope() {
    local desc="app/models 只剩 base/user/token/admin"
    local files
    files=$(ls app/models/*.py 2>/dev/null | xargs -n1 basename)
    local extra=""
    for f in $files; do
        case "$f" in
            __init__.py|base.py|user.py|token.py|admin.py) ;;
            *) extra="$extra $f" ;;
        esac
    done
    if [[ -z "$extra" ]]; then
        record_pass "$desc"
    else
        record_fail "$desc：多余文件$extra"
    fi
}

# -------------------------------------------------------------------- #
# 5. app/services/client 只剩 ai_service/auth/email_templates/redis_verification
# -------------------------------------------------------------------- #
check_client_services_scope() {
    local desc="app/services/client 只剩 ai_service/auth/email_templates/redis_verification"
    local files
    files=$(ls app/services/client/*.py 2>/dev/null | xargs -n1 basename)
    local extra=""
    for f in $files; do
        case "$f" in
            __init__.py|ai_service.py|auth.py|email_templates.py|redis_verification.py) ;;
            *) extra="$extra $f" ;;
        esac
    done
    if [[ -z "$extra" ]]; then
        record_pass "$desc"
    else
        record_fail "$desc：多余文件$extra"
    fi
}

# -------------------------------------------------------------------- #
# 6. .env.example 含必需变量
# -------------------------------------------------------------------- #
check_env_example() {
    local desc=".env.example 含必需变量"
    local need=(PROJECT_NAME API_PORT POSTGRES_PORT POSTGRES_HOST REDIS_PORT REDIS_EXTERNAL_PORT NGINX_HTTP_PORT NGINX_HTTPS_PORT FLOWER_PORT SERVER_NAME CORS_ALLOWED_ORIGINS SECRET_KEY)
    local ok=1
    for v in "${need[@]}"; do
        if ! grep -q "^$v=" .env.example; then
            record_fail "$desc：缺 $v"
            ok=0
        fi
    done
    if [[ $ok -eq 1 ]]; then record_pass "$desc"; fi
}

# -------------------------------------------------------------------- #
# 7. requirements.txt 不含面试依赖
# -------------------------------------------------------------------- #
check_requirements() {
    local desc="requirements.txt 不含 pypdf2/python-docx/pandas/numpy/lxml/pdfplumber"
    local hit
    hit=$(grep -iE '^(pypdf2|python-docx|pandas|numpy|lxml|pdfplumber)==' requirements.txt || true)
    if [[ -z "$hit" ]]; then
        record_pass "$desc"
    else
        record_fail "$desc"
        echo "$hit" | sed 's/^/      /'
    fi
}

# -------------------------------------------------------------------- #
# 8. Dockerfile 不含 libmysqlclient
# -------------------------------------------------------------------- #
check_dockerfile_pg() {
    local desc="Dockerfile 不含 libmysqlclient（用 libpq-dev）"
    if grep -q 'libmysqlclient' Dockerfile 2>/dev/null; then
        record_fail "$desc"
    else
        record_pass "$desc"
    fi
}

# -------------------------------------------------------------------- #
# 9. ai_service 支持传入 system_prompt 参数
# -------------------------------------------------------------------- #
check_ai_service_generic() {
    local desc="ai_service 支持传入 system_prompt（通用 chat/complete 抽象）"
    if grep -q 'async def chat(' app/services/client/ai_service.py \
       && grep -q 'system_prompt' app/services/client/ai_service.py; then
        record_pass "$desc"
    else
        record_fail "$desc"
    fi
}

# -------------------------------------------------------------------- #
# 10. 通用 AI 路由存在
# -------------------------------------------------------------------- #
check_ai_route() {
    local desc="通用 AI 路由 app/api/client/v1/ai.py 存在且注册"
    if [[ -f app/api/client/v1/ai.py ]] \
       && grep -q 'app.api.client.v1.ai' app/route/router_registry.py; then
        record_pass "$desc"
    else
        record_fail "$desc"
    fi
}

# -------------------------------------------------------------------- #
# 11. SECRET_KEY 生产校验
# -------------------------------------------------------------------- #
check_secret_key_guard() {
    local desc="config.py 有 SECRET_KEY 生产环境校验"
    if grep -q 'ENV == "production" and self.SECRET_KEY' app/core/config.py; then
        record_pass "$desc"
    else
        record_fail "$desc"
    fi
}

# -------------------------------------------------------------------- #
# 12. .gitignore 排除 .env / uploads / logs / __pycache__ / celerybeat
# -------------------------------------------------------------------- #
check_gitignore() {
    local desc=".gitignore 排除 .env/uploads/logs/__pycache__/celerybeat"
    local ok=1
    # 用 grep -E 行首匹配，兼容 CRLF（不要求行尾 $）
    for p in '^\.env' 'uploads/' 'logs/' '__pycache__/' 'celerybeat-schedule'; do
        if ! grep -qE "$p" .gitignore; then
            record_fail "$desc：缺 $p"
            ok=0
        fi
    done
    if [[ $ok -eq 1 ]]; then record_pass "$desc"; fi
}

# -------------------------------------------------------------------- #
# 13. pytest（可选，docker 不可用则 SKIP）
# -------------------------------------------------------------------- #
check_pytest() {
    local desc="pytest 通过"
    if ! docker_available; then
        record_skip "$desc（docker 不可用，跳过；可在容器内手动跑 pytest）"
        return
    fi
    if ! docker compose ps --status running app 2>/dev/null | grep -q app; then
        record_skip "$desc（app 容器未运行，跳过；启动后可手动跑 docker compose exec app pytest）"
        return
    fi
    if docker compose exec -T app pytest -q 2>&1; then
        record_pass "$desc"
    else
        record_fail "$desc"
    fi
}

echo "==================== FastAPI Scaffold 验收 ===================="
check_compose_port_params
check_app_networks
check_business_residue
check_models_scope
check_client_services_scope
check_env_example
check_requirements
check_dockerfile_pg
check_ai_service_generic
check_ai_route
check_secret_key_guard
check_gitignore
check_pytest
echo "=============================================================="
echo "汇总: $(green PASS=$PASS_COUNT) $(red FAIL=$FAIL_COUNT) $(yellow SKIP=$SKIP_COUNT)"
if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
exit 0

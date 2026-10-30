#!/usr/bin/env bash
# kb.sh — DeepSeek Harness 个人知识库 终端访问脚本
#
# 用法:
#   ./kb.sh list              列出全部条目
#   ./kb.sh <主题>            抓取指定文档（如 ./kb.sh architecture）
#   ./kb.sh search <关键词>   全库搜索（优先本地缓存，否则远程全文）
#   ./kb.sh update            刷新本地缓存
#
# 原理: 通过 GitHub raw 链接抓取本知识库的 Markdown 文件，无需登录。
# 兼容: bash 3.2+（macOS 系统自带 bash 可直接运行），不依赖关联数组。

set -euo pipefail

BASE="https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main"
JSDELIVR="https://cdn.jsdelivr.net/gh/xiexie512/deepseek-harness-kb@main"
API="https://api.github.com/repos/xiexie512/deepseek-harness-kb/contents"
CACHE_DIR="${KB_CACHE_DIR:-$HOME/.cache/dsh-kb}"
CURL_OPTS=(-fsSL --connect-timeout 8 --max-time 20)

# 校验下载内容确为 Markdown（首行以 # 开头），防止拿到重定向/错误页
is_md() { head -c 1 "$1" 2>/dev/null | grep -q "#"; }

try_raw() { curl "${CURL_OPTS[@]}" "$BASE/$1" -o "$2" 2>/dev/null && is_md "$2"; }

try_jsdelivr() { curl "${CURL_OPTS[@]}" "$JSDELIVR/$1" -o "$2" 2>/dev/null && is_md "$2"; }

TOPICS="overview quickstart cli architecture plugins configuration models sdk glossary dsh-pet dsh-phone qqbot douyin-bot workspace-sync zhipu-model-label setup llms full"

# 主题 → 文件路径（新增文档时在此登记）
path_for() {
  case "$1" in
    overview)          echo "docs/overview.md" ;;
    quickstart)        echo "docs/quickstart.md" ;;
    cli)               echo "docs/cli.md" ;;
    architecture)      echo "docs/architecture.md" ;;
    plugins)           echo "docs/plugins.md" ;;
    configuration)     echo "docs/configuration.md" ;;
    models)            echo "docs/models.md" ;;
    sdk)               echo "docs/sdk.md" ;;
    glossary)          echo "docs/glossary.md" ;;
    dsh-pet)           echo "projects/dsh-pet.md" ;;
    dsh-phone)         echo "projects/dsh-phone.md" ;;
    qqbot)             echo "projects/qqbot.md" ;;
    douyin-bot)        echo "projects/douyin-bot.md" ;;
    workspace-sync)    echo "projects/workspace-sync.md" ;;
    zhipu-model-label) echo "projects/zhipu-model-label.md" ;;
    setup)             echo "notes/setup.md" ;;
    llms)              echo "llms.txt" ;;
    full)              echo "llms-full.txt" ;;
    *)                 echo "" ;;
  esac
}

fetch() { # $1=remote_path → stdout；多源自动回退
  local path="$1" tmp
  tmp="$(mktemp)"
  if try_raw "$path" "$tmp" || try_jsdelivr "$path" "$tmp" || try_api "$path" "$tmp"; then
    cat "$tmp"
    rm -f "$tmp"
    return 0
  fi
  rm -f "$tmp"
  echo "抓取失败（raw / jsDelivr / api.github.com 均不可达）: $path" >&2
  return 1
}

try_api() { # GitHub Contents API：返回 base64 JSON，用 python3/base64 解码
  local json
  json="$(curl "${CURL_OPTS[@]}" "$API/$1" 2>/dev/null)" || return 1
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "$json" | python3 -c 'import sys,json,base64;print(base64.b64decode(json.load(sys.stdin)["content"]).decode("utf-8"),end="")' > "$2" 2>/dev/null
  else
    printf '%s' "$json" | python3 - 2>/dev/null <<'PY'
import sys, json, base64
print(base64.b64decode(json.load(sys.stdin)["content"]).decode("utf-8"), end="")
PY
  fi
}

cmd_list() {
  echo "DeepSeek Harness 知识库条目："
  local t
  for t in $TOPICS; do
    printf '  %-18s %s\n' "$t" "$(path_for "$t")"
  done
  echo
  echo "用法: ./kb.sh <主题> | search <关键词> | update"
}

cmd_get() { # $1=topic
  local key="$1" path
  path="$(path_for "$key")"
  if [ -z "$path" ]; then
    echo "未知主题: ${key}（用 ./kb.sh list 查看全部）" >&2
    exit 1
  fi
  fetch "$path"
}

cmd_search() { # $1=keyword
  local kw="$1" tmp newtmp
  [ -n "$kw" ] || { echo "用法: ./kb.sh search <关键词>" >&2; exit 1; }
  mkdir -p "$CACHE_DIR"
  tmp="$CACHE_DIR/llms-full.txt"
  if [ ! -s "$tmp" ]; then
    echo "首次使用，刷新全文缓存…" >&2
    cmd_update
  fi
  echo "匹配 “${kw}” 的片段："
  grep -n -i -- "$kw" "$tmp" || { echo "（无匹配，可先 ./kb.sh update 刷新缓存）"; exit 1; }
}

cmd_update() {
  local newtmp
  mkdir -p "$CACHE_DIR"
  echo "刷新全文缓存到 $CACHE_DIR …" >&2
  newtmp="$(mktemp)"
  fetch "llms-full.txt" > "$newtmp"
  mv -f "$newtmp" "$CACHE_DIR/llms-full.txt"
  echo "已刷新 llms-full.txt 缓存（$CACHE_DIR/llms-full.txt）"
}

case "${1:-}" in
  list)   cmd_list ;;
  search) cmd_search "${2:-}" ;;
  update) cmd_update ;;
  "")     cmd_list ;;
  *)      cmd_get "$1" ;;
esac

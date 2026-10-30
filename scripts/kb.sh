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

set -euo pipefail

BASE="https://raw.githubusercontent.com/xiexie512/deepseek-harness-kb/main"
CACHE_DIR="${KB_CACHE_DIR:-$HOME/.cache/dsh-kb}"

# 主题 → 文件路径 映射（新增文档时在此登记）
declare -A FILES=(
  [overview]="docs/overview.md"
  [quickstart]="docs/quickstart.md"
  [cli]="docs/cli.md"
  [architecture]="docs/architecture.md"
  [plugins]="docs/plugins.md"
  [configuration]="docs/configuration.md"
  [models]="docs/models.md"
  [sdk]="docs/sdk.md"
  [glossary]="docs/glossary.md"
  [dsh-pet]="projects/dsh-pet.md"
  [dsh-phone]="projects/dsh-phone.md"
  [qqbot]="projects/qqbot.md"
  [douyin-bot]="projects/douyin-bot.md"
  [workspace-sync]="projects/workspace-sync.md"
  [zhipu-model-label]="projects/zhipu-model-label.md"
  [setup]="notes/setup.md"
  [llms]="llms.txt"
  [full]="llms-full.txt"
)

fetch() { # $1=remote_path
  local path="$1" url="$BASE/$path"
  curl -fsSL --connect-timeout 10 "$url" || { echo "抓取失败: $url" >&2; exit 1; }
}

cmd_list() {
  echo "DeepSeek Harness 知识库条目："
  for k in overview quickstart cli architecture plugins configuration models sdk glossary \
           dsh-pet dsh-phone qqbot douyin-bot workspace-sync zhipu-model-label setup llms full; do
    printf '  %-18s %s\n' "$k" "${FILES[$k]}"
  done
  echo
  echo "用法: ./kb.sh <主题> | search <关键词> | update"
}

cmd_get() { # $1=topic
  local key="$1" path
  path="${FILES[$key]:-}"
  if [ -z "$path" ]; then
    echo "未知主题: $key（用 ./kb.sh list 查看全部）" >&2
    exit 1
  fi
  fetch "$path"
}

cmd_search() { # $1=keyword
  local kw="$1" tmp
  [ -n "$kw" ] || { echo "用法: ./kb.sh search <关键词>" >&2; exit 1; }
  mkdir -p "$CACHE_DIR"
  tmp="$CACHE_DIR/llms-full.txt"
  if [ ! -f "$tmp" ] || [ "$(find "$tmp" -mtime +1 2>/dev/null | wc -l | tr -d ' ')" = "1" ]; then
    echo "刷新全文缓存…" >&2
    fetch "llms-full.txt" > "$tmp"
  fi
  echo "匹配 “$kw” 的片段："
  grep -n -i -- "$kw" "$tmp" || { echo "（无匹配）"; exit 1; }
}

cmd_update() {
  mkdir -p "$CACHE_DIR"
  echo "缓存到 $CACHE_DIR …" >&2
  fetch "llms-full.txt" > "$CACHE_DIR/llms-full.txt"
  echo "已刷新 llms-full.txt 缓存（$CACHE_DIR/llms-full.txt）"
}

case "${1:-}" in
  list)   cmd_list ;;
  search) cmd_search "${2:-}" ;;
  update) cmd_update ;;
  "")     cmd_list ;;
  *)      cmd_get "$1" ;;
esac

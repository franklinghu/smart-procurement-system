#!/bin/bash
# 自动提交并推送脚本
# 用法: ./scripts/auto-commit.sh "commit message"

cd "$(dirname "$0")/.." || exit 1

MSG="${1:-update: $(date '+%Y-%m-%d %H:%M')}"

# 添加所有更改
git add -A

# 检查是否有更改
if git diff --cached --quiet; then
    echo "没有需要提交的更改"
    exit 0
fi

# 提交
git commit -m "$MSG"

# 推送
echo "正在推送到 GitHub..."
git push origin main

echo "✅ 同步完成!"
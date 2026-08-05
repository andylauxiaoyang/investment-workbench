#!/usr/bin/env bash
# 投资工作台 · 每日自动更新（push 到 Gitee/GitHub，Pages 开启“自动部署”即自动更新线上）
# 注意：token 只通过环境变量注入（GITEE_TOKEN / GITHUB_TOKEN），绝不硬编码。
set -e

DEPLOY="/d/invdeploy"
GITEE_USER="${GITEE_USER:-andylauxiaoyang}"
REPO="${GITEE_REPO:-investment-workbench}"
BRANCH="master"

# 可选：先同步最新持仓到 deploy 目录（需 ttskill + node 环境；不设 SYNC=1 则跳过）
if [ "${SYNC}" = "1" ]; then
  WS="/d/workbuddy下载/投资工作台"
  echo "== 同步持仓 =="
  node "$WS/sync-holdings.js" || { echo "SYNC_FAIL"; exit 1; }
  cp "$WS/investment-workbench.html" "$DEPLOY/index.html"
  cp "$WS/holdings-data.json"        "$DEPLOY/holdings-data.json"
fi

cd "$DEPLOY"
git add -A
if git diff --cached --quiet; then
  echo "（无变更，跳过推送）"
  exit 0
fi
git commit -q -m "sync: $(date +%Y-%m-%dT%H:%M)"

if [ -n "${GITEE_TOKEN}" ]; then
  echo "== push to Gitee =="
  git push "https://${GITEE_USER}:${GITEE_TOKEN}@gitee.com/${GITEE_USER}/${REPO}.git" "HEAD:${BRANCH}"
elif [ -n "${GITHUB_TOKEN}" ]; then
  GH_USER="${GITHUB_USER:-andylauxiaoyang}"
  echo "== push to GitHub =="
  git push "https://${GH_USER}:${GITHUB_TOKEN}@github.com/${GH_USER}/${REPO}.git" "HEAD:${BRANCH}"
else
  echo "ERROR: 需设置 GITEE_TOKEN 或 GITHUB_TOKEN"; exit 1
fi
echo "DONE"

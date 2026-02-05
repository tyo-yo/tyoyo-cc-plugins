---
name: ntfy-claude-runner
description: This skill should be used when the user asks to "set up ntfy claude", "configure event-driven claude", "set up notification-triggered claude", "automate claude with triggers", "run claude from notifications", or needs to set up a system where external events (Slack, Gmail, cron, webhooks) automatically trigger Claude Code sessions in Zellij terminal panes.
---

# ntfy-claude-runner: Event-Driven Claude Code Execution

外部イベント（Slack, Gmail, cron, webhook 等）をトリガーに、Zellij ターミナルペイン上で Claude Code セッションを自動起動するシステム。

## システム概要

```
[外部トリガー]          [ローカル Mac]
  n8n / Zapier          ntfy-claude-daemon.py
  cron / curl     →     (ntfy subscribe)
  Slack / Gmail           ↓
       |            Zellij ペイン生成
       v                  ↓
   ntfy.sh           Claude Code 起動
  (中継サーバー)      (interactive / auto)
```

## コンポーネント

| ファイル | 役割 |
|---------|------|
| `resources/ntfy-claude-daemon.py` | メインデーモン（Python, uv run） |
| `resources/claude-tasks.kdl` | Zellij レイアウト（最大20ペイン対応） |
| `resources/com.user.ntfy-claude.plist` | launchd 設定テンプレート |

## セットアップ

セットアップが必要な場合は `SETUP.md` を参照すること。

## 使い方

### メッセージ送信（トリガー側）

```bash
# Interactive: Zellij ペインで Claude が対話モードで起動
curl -d "Fix the auth bug in src/login.ts" ntfy.sh/<YOUR_TOPIC>

# Auto: Claude が自動実行して完了
curl -d '{"type":"auto","prompt":"Summarize README.md"}' ntfy.sh/<YOUR_TOPIC>
```

### タスクタイプ

| タイプ | 動作 | Claude の起動方法 |
|--------|------|------------------|
| `interactive` | ペインが開いてユーザーが対話 | `claude "prompt"` |
| `auto` | 自動実行して完了 | `claude -p "prompt" --max-turns 10` |

プレーンテキストのメッセージは `interactive` として扱われる。

### JSON ペイロード形式

```json
{
  "type": "auto",
  "prompt": "Run tests and report results"
}
```

### デーモン管理

```bash
# 手動起動
NTFY_TOPIC=<YOUR_TOPIC> uv run resources/ntfy-claude-daemon.py

# launchd で起動
launchctl load ~/Library/LaunchAgents/com.user.ntfy-claude.plist

# 停止
launchctl unload ~/Library/LaunchAgents/com.user.ntfy-claude.plist

# ログ確認
tail -f ~/.local/share/ntfy-claude/stderr.log
```

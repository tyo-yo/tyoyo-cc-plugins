---
name: ntfy-claude-runner
description: This skill should be used when the user asks to "set up ntfy claude", "configure event-driven claude", "set up notification-triggered claude", "automate claude with triggers", "run claude from notifications", or needs to set up a system where external events (Slack, Gmail, cron, webhooks) automatically trigger Claude Code sessions in Zellij terminal panes.
---

# ntfy-claude-runner: Event-Driven Claude Code Execution

外部イベント（Slack, Gmail, cron, webhook 等）をトリガーに、Claude Code セッションを自動実行するシステム。
TUI ダッシュボードで auto タスクの一覧表示・詳細表示・接続状態を確認できる。

## セキュリティに関する注意

**ntfy トピック名はパスワード相当の秘匿情報である。**
Claude はトピック名を知る必要がなく、知るべきでもない。
セットアップ・動作確認・トラブルシューティングのすべてにおいて、
コマンドの実行はユーザー自身が別ターミナルで行うこと。
Claude がこのスキルで行うのは「手順の案内」のみである。

## システム概要

```
[外部トリガー]          [ローカル Mac]
  n8n / Zapier          ntfy-claude-daemon.py
  cron / curl     →     (ntfy subscribe)
  Slack / Gmail           ↓
       |            ┌─ TUI ダッシュボード ─┐
       v            │ auto: 一覧+詳細表示   │
   ntfy.sh          │ interactive: Zellij   │
  (中継サーバー)     └────────────────────┘
```

## タスクタイプ

| タイプ | 動作 | 実行方法 |
|--------|------|----------|
| `auto` | TUI 内で自動実行、結果をダッシュボードに表示 | `claude -p "prompt" --output-format json --max-turns 10` |
| `interactive` | Zellij ペインを開いてユーザーが対話 | `claude "prompt"` |

プレーンテキストのメッセージは `interactive` として扱われる。

## TUI ダッシュボード

デーモンは Textual TUI として起動する。

### 一覧画面（デフォルト）
- auto タスクのみ表示（interactive は Zellij ペインに直接送られる）
- 各行: ステータスアイコン + プロンプト + 日時
- キーバインド: `Enter`=詳細表示, `r`=リフレッシュ, `q`=終了

### 詳細画面
- Claude の出力結果を Markdown レンダリングで表示
- コスト・実行時間をメタバーに表示
- `Escape` / `q` で一覧に戻る

## コンポーネント

| ファイル | 役割 |
|---------|------|
| `resources/ntfy-claude-daemon.py` | メインデーモン（Textual TUI, uv run） |
| `resources/claude-tasks.kdl` | Zellij レイアウト（最大20ペイン対応） |
| `resources/com.user.ntfy-claude.plist` | launchd 設定テンプレート |

## セットアップ

セットアップが必要な場合は `SETUP.md` を参照し、手順をユーザーに案内すること。
**Claude 自身がコマンドを実行してはならない。**

## 使い方の案内

ユーザーに以下の情報を伝えること。コマンド例の `$NTFY_TOPIC` はユーザーの環境変数が展開される前提。

### メッセージ送信（トリガー側）

```bash
# Interactive: Zellij ペインで Claude が対話モードで起動
curl -d "Fix the auth bug in src/login.ts" "ntfy.sh/$NTFY_TOPIC"

# Auto: TUI ダッシュボード内で自動実行、結果を表示
curl -d '{"type":"auto","prompt":"Summarize README.md"}' "ntfy.sh/$NTFY_TOPIC"
```

### デーモン管理（ユーザーが別ターミナルで実行）

```bash
# TUI ダッシュボードを起動（alias はセットアップ時に登録済み）
ntfy-claude

# 環境変数でカスタマイズ可能
CLAUDE_TIMEOUT=300 ntfy-claude   # タイムアウトを5分に変更
```

### ジョブ履歴

auto タスクの実行結果は `~/.local/share/ntfy-claude/jobs.jsonl` に JSONL 形式で永続化される。
TUI 起動時に履歴をロードして表示する。

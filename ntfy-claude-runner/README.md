# ntfy-claude-runner

外部イベントをトリガーに、Zellij ターミナルペイン上で Claude Code セッションを自動起動するシステム。

## 目的

Slack メッセージ、Gmail 受信、cron ジョブ、webhook など、あらゆるイベントをきっかけに Claude Code を自動実行したい。ただし Claude Code の**サブスクリプション認証**を使いたいので、API キーが必要な Agent SDK ではなく、`claude` CLI をそのまま叩く方式を採用。

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│ External Triggers                                       │
│                                                         │
│  n8n / Zapier / IFTTT    cron    Slack Bot    手動 curl  │
│         │                  │        │            │      │
│         └──────────┬───────┴────────┴────────────┘      │
│                    │                                    │
│                    v                                    │
│            ┌──────────────┐                             │
│            │   ntfy.sh    │  ← HTTP POST で通知を中継   │
│            │  (クラウド)   │  ← トピック名 = パスワード  │
│            └──────┬───────┘                             │
│                   │                                     │
└───────────────────┼─────────────────────────────────────┘
                    │ JSON stream (SSE)
                    v
┌───────────────────────────────────────────────────────────┐
│ Local Mac                                                 │
│                                                           │
│  ┌─────────────────────────────┐                          │
│  │ ntfy-claude-daemon.py       │  ← uv run で起動        │
│  │ (httpx streaming + sh)      │  ← launchd で常駐化     │
│  └──────────┬──────────────────┘                          │
│             │                                             │
│             │ zellij --session main run -- claude "prompt" │
│             v                                             │
│  ┌──────────────────────────────────────────────┐         │
│  │ Zellij (session: main)                       │         │
│  │                                              │         │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │         │
│  │  │ Claude   │ │ Claude   │ │ Claude   │     │         │
│  │  │ (task 1) │ │ (task 2) │ │ (task 3) │     │         │
│  │  └──────────┘ └──────────┘ └──────────┘     │         │
│  │  ... 最大 20 ペインまでタイルド表示 ...        │         │
│  └──────────────────────────────────────────────┘         │
└───────────────────────────────────────────────────────────┘
```

## コンポーネント

| ファイル | 説明 |
|---------|------|
| `skills/.../resources/ntfy-claude-daemon.py` | メインデーモン（~120行, Python） |
| `skills/.../resources/claude-tasks.kdl` | Zellij カスタムレイアウト（20ペイン対応） |
| `skills/.../resources/com.user.ntfy-claude.plist` | launchd 設定テンプレート |
| `skills/.../SETUP.md` | セットアップ手順 |
| `skills/.../SKILL.md` | Claude Code スキル定義 |

## 技術スタック

- **ntfy.sh**: HTTP ベースの Pub/Sub（無料、登録不要）
- **Python + uv**: デーモンスクリプト（httpx, sh ライブラリ）
- **Zellij**: ターミナルマルチプレクサー（ペイン管理）
- **Claude Code CLI**: `claude` / `claude -p`（サブスクリプション認証）
- **launchd**: macOS ネイティブのデーモン管理

## クイックスタート

```bash
# 1. ランダムなトピック名を生成（自分で実行して保管）
echo "ntfy-claude-$(openssl rand -hex 8)"

# 2. デーモン起動
NTFY_TOPIC=<生成したトピック名> uv run skills/ntfy-claude-runner/resources/ntfy-claude-daemon.py

# 3. 別ターミナルからテスト
curl -d "hello test" ntfy.sh/<生成したトピック名>
```

## 設計判断

| 判断 | 理由 |
|------|------|
| ntfy.sh を中継に使う | トピック名がパスワード代わり。登録不要。無料。12時間メッセージキャッシュ |
| Python + uv（Bun/Shell ではなく） | PEP 723 で依存を自己完結。`sh` ライブラリでシェルコマンドが自然に書ける |
| launchd で常駐化 | macOS ネイティブ。スクリプト側でデーモン化コード不要 |
| Zellij ペインで表示 | ユーザーの作業ターミナルに直接統合。進行状況が見える |
| auto / interactive の2タイプ | 定型タスクは自動実行、判断が必要なタスクは対話モード |

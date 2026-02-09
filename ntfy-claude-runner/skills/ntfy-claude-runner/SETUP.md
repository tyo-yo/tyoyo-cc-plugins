# ntfy-claude-runner セットアップガイド

> **このガイドに含まれるコマンドはすべてユーザー自身が別ターミナルで実行すること。**
> Claude はトピック名を含む秘匿情報に触れないよう設計されている。
> Claude の役割は手順の案内とトラブルシューティングのみ。

## 前提条件

以下がインストール済みであること（別ターミナルで確認）:

```bash
which uv       # Python パッケージマネージャー
which zellij   # ターミナルマルチプレクサー（interactive タスク用）
which claude   # Claude Code CLI
```

未インストールの場合:

```bash
# uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# zellij（interactive タスクを使う場合のみ必要）
brew install zellij

# claude (Claude Code)
# https://docs.anthropic.com/en/docs/claude-code
```

### 依存パッケージ

デーモンは `uv run --script` で実行されるため、依存パッケージは自動インストールされる:

- `textual>=1.0` — TUI フレームワーク（rich を内包）
- `httpx` — HTTP クライアント（ntfy.sh ストリーム購読）
- `sh>=2.0` — シェルコマンドラッパー（Zellij 操作）

---

## Step 1: 初期設定

**以下を別ターミナルで実行すること。**

### 1-1. ntfy トピック名の生成

セキュリティのため、推測されにくいランダムなトピック名を使う。

```bash
NTFY_TOPIC="ntfy-claude-$(openssl rand -hex 8)" && echo "export NTFY_TOPIC=\"$NTFY_TOPIC\"" >> ~/.zshrc && export NTFY_TOPIC && echo "Done"
```

> **重要**: トピック名は ntfy.sh 上で認証なしにアクセスできるため、ランダムな文字列をパスワード代わりに使う。トピック名を第三者や Claude に共有しないこと。

### 1-2. デーモン起動コマンドの登録

```bash
echo "alias ntfy-claude='uv run https://raw.githubusercontent.com/tyo-yo/tyoyo-cc-plugins/main/ntfy-claude-runner/skills/ntfy-claude-runner/resources/ntfy-claude-daemon.py'" >> ~/.zshrc && source <(echo "alias ntfy-claude='uv run https://raw.githubusercontent.com/tyo-yo/tyoyo-cc-plugins/main/ntfy-claude-runner/skills/ntfy-claude-runner/resources/ntfy-claude-daemon.py'") && echo "Done"
```

---

## Step 2: 動作確認

**ターミナル A** でデーモンをフォアグラウンド起動:

```bash
ntfy-claude
```

TUI ダッシュボードが表示され、ステータスバーに「Connected」と表示されることを確認。

**ターミナル B** からテスト送信:

```bash
# auto タスク（TUI に結果が表示される）
curl -d '{"type":"auto","prompt":"Say hello"}' "ntfy.sh/$NTFY_TOPIC"

# interactive タスク（Zellij ペインが開く。Zellij セッションが必要）
curl -d "hello test" "ntfy.sh/$NTFY_TOPIC"
```

auto タスクの場合: TUI の一覧に「⏳ → >> → OK」とステータスが遷移し、Enter で詳細表示できれば成功。

確認後、TUI で `q` を押して終了する。

---

## Step 3: Zellij レイアウトの配置（interactive タスクを使う場合）

デフォルトの Zellij レイアウトは12ペインまでしかタイルド表示しない。
20ペインまで対応するカスタムレイアウトを使う場合:

**別ターミナルで実行:**

```bash
mkdir -p ~/.config/zellij/layouts
cp "${CLAUDE_PLUGIN_ROOT}/skills/ntfy-claude-runner/resources/claude-tasks.kdl" \
   ~/.config/zellij/layouts/
```

このレイアウトを使ってセッションを起動:

```bash
zellij --layout claude-tasks --session main
```

---

## Step 4: launchd でデーモン化（任意）

> **注意**: TUI モードは TTY が必要なため、launchd での自動起動には向かない。
> launchd を使う場合は headless モード（将来検討）が必要。
> 現時点ではターミナルでの手動起動を推奨する。

従来の launchd 設定を使いたい場合は `com.user.ntfy-claude.plist` テンプレートを参照。
ただし、TUI が表示されないためログ確認のみの用途となる。

---

## トラブルシューティング

### TUI が表示されない / 文字化けする

ターミナルが True Color に対応していることを確認。以下のターミナルを推奨:
- iTerm2
- WezTerm
- Ghostty
- kitty

### Zellij セッション "main" が見つからない（interactive タスク）

デーモンは既存の Zellij セッションにペインを追加する。セッションが存在しない場合はエラーになる。

```bash
# セッション一覧確認
zellij list-sessions

# セッションが無ければ起動
zellij --session main
```

### ntfy.sh への接続が切れる

デーモンは自動再接続する（指数バックオフ: 1s → 2s → 4s → ... → 60s）。
ステータスバーに「Disconnected」と表示されるが、再接続後は自動で「Connected」に復帰する。
再接続時に `since=` パラメータで未処理メッセージをキャッチアップする。

### Mac スリープ後にメッセージが漏れる

ntfy.sh はメッセージを12時間キャッシュする。スリープ復帰後の再接続時に
`since=<最後のタイムスタンプ>` でキャッチアップするため、12時間以内のスリープなら漏れない。

### auto タスクがタイムアウトする

デフォルトのタイムアウトは10分（600秒）。変更する場合:

```bash
CLAUDE_TIMEOUT=300 ntfy-claude   # 5分に変更
```

### Claude の権限設定

デフォルトでは安全な自動実行モード（`--permission-mode acceptEdits` + `--allowedTools`）で動作する。

```bash
# 許可するツールをカスタマイズ
CLAUDE_ALLOWED_TOOLS="Bash,Read,Edit" ntfy-claude

# 完全自動モード（隔離環境でのみ推奨）
CLAUDE_SKIP_PERMISSIONS=1 ntfy-claude
```

| 環境変数 | デフォルト | 説明 |
|---------|-----------|------|
| `CLAUDE_ALLOWED_TOOLS` | `Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch` | 自動許可するツール |
| `CLAUDE_SKIP_PERMISSIONS` | (未設定) | `1` で全権限スキップ |

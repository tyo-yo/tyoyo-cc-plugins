# ntfy-claude-runner セットアップガイド

## 前提条件

以下がインストール済みであること:

```bash
# 確認コマンド
which uv       # Python パッケージマネージャー
which zellij   # ターミナルマルチプレクサー
which claude   # Claude Code CLI
```

未インストールの場合:

```bash
# uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# zellij
brew install zellij

# claude (Claude Code)
# https://docs.anthropic.com/en/docs/claude-code
```

---

## Step 1: ntfy トピック名の生成

セキュリティのため、推測されにくいランダムなトピック名を使う。
**以下のコマンドをユーザー自身で実行し、結果を安全に保管すること。**

```bash
# ランダムなトピック名を生成
echo "ntfy-claude-$(openssl rand -hex 8)"
```

生成されたトピック名を `.zshrc` や `.bashrc` に環境変数として設定:

```bash
# .zshrc に追加（ユーザーが手動で実行）
echo 'export NTFY_CLAUDE_TOPIC="<生成したトピック名>"' >> ~/.zshrc
source ~/.zshrc
```

> **重要**: トピック名は ntfy.sh 上で認証なしにアクセスできるため、ランダムな文字列をパスワード代わりに使う。トピック名を第三者に共有しないこと。

---

## Step 2: デーモンスクリプトの配置

```bash
# スクリプトを配置
mkdir -p ~/scripts
cp "${CLAUDE_PLUGIN_ROOT}/skills/ntfy-claude-runner/resources/ntfy-claude-daemon.py" ~/scripts/
chmod +x ~/scripts/ntfy-claude-daemon.py
```

動作確認（フォアグラウンドで実行）:

```bash
NTFY_TOPIC="$NTFY_CLAUDE_TOPIC" uv run ~/scripts/ntfy-claude-daemon.py
```

別のターミナルからテスト送信:

```bash
curl -d "hello test" "ntfy.sh/$NTFY_CLAUDE_TOPIC"
```

Zellij の "main" セッションに新しいペインが開いて Claude Code が起動すれば成功。

---

## Step 3: Zellij レイアウトの配置（任意）

デフォルトの Zellij レイアウトは12ペインまでしかタイルド表示しない。
20ペインまで対応するカスタムレイアウトを使う場合:

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

ログイン時に自動起動し、クラッシュ時に自動復旧させる。

### 4-1. plist テンプレートをコピー

```bash
cp "${CLAUDE_PLUGIN_ROOT}/skills/ntfy-claude-runner/resources/com.user.ntfy-claude.plist" \
   ~/Library/LaunchAgents/
```

### 4-2. plist 内のプレースホルダーを置換

以下のコマンドで各値を確認し、plist を編集:

```bash
echo "UV_PATH: $(which uv)"
echo "HOME: $HOME"
echo "PATH: $PATH"
echo "TOPIC: $NTFY_CLAUDE_TOPIC"
echo "SCRIPT: $HOME/scripts/ntfy-claude-daemon.py"
```

**ユーザーが `~/Library/LaunchAgents/com.user.ntfy-claude.plist` を手動で編集して、
`__UV_PATH__`, `__HOME__`, `__PATH__`, `__NTFY_TOPIC__`, `__DAEMON_SCRIPT_PATH__` を
上記の値で置換すること。**

### 4-3. ログディレクトリの作成

```bash
mkdir -p ~/.local/share/ntfy-claude
```

### 4-4. 起動

```bash
launchctl load ~/Library/LaunchAgents/com.user.ntfy-claude.plist
```

### 4-5. 確認

```bash
# 起動確認
launchctl list | grep ntfy-claude

# ログ確認
tail -f ~/.local/share/ntfy-claude/stderr.log
```

---

## トラブルシューティング

### Zellij セッション "main" が見つからない

デーモンは既存の Zellij セッションにペインを追加する。セッションが存在しない場合はエラーになる。

```bash
# セッション一覧確認
zellij list-sessions

# セッションが無ければ起動
zellij --session main
```

### ntfy.sh への接続が切れる

デーモンは自動再接続する（指数バックオフ: 1s → 2s → 4s → ... → 60s）。
再接続時に `since=` パラメータで未処理メッセージをキャッチアップする。

### Mac スリープ後にメッセージが漏れる

ntfy.sh はメッセージを12時間キャッシュする。スリープ復帰後の再接続時に
`since=<最後のタイムスタンプ>` でキャッチアップするため、12時間以内のスリープなら漏れない。

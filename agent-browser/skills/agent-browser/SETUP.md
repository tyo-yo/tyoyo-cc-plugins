# agent-browser セットアップガイド

このガイドでは、agent-browser と CDP 接続環境のセットアップ方法を説明します。

## 1. agent-browser のインストール

公式: https://github.com/vercel-labs/agent-browser

```bash
npm install -g agent-browser
```

インストール確認:
```bash
which agent-browser
agent-browser --help
```

ブラウザバイナリのインストール（初回のみ）:
```bash
agent-browser install
```

---

## 2. CDP 接続用 Chrome 環境の準備

### なぜ専用プロファイルが必要か

Chrome v136 以降、セキュリティ強化により **デフォルトプロファイルでの CDP 接続がブロック** されるようになりました。

- `--remote-debugging-port` を指定しても、デフォルトプロファイルではポートが開かない
- `--user-data-dir` で **別のディレクトリを指定する必要がある**

そのため、既存の Chrome プロファイルを専用ディレクトリにコピーし、そこから CDP モードで起動します。

### プロファイルのコピー（初回のみ）

```bash
# 専用プロファイルディレクトリを作成
ditto "$HOME/Library/Application Support/Google/Chrome" "$HOME/.chrome-automation-profile"
```

**注意**: 数GBのコピーになるため、数分かかる場合があります。

---

## 3. chrome-debug コマンドの設定

`.zshrc` または `.bashrc` に以下を追加:

```bash
# Chrome CDP debug mode (for agent-browser)
# 永続的な専用プロファイルを使用（初回のみコピー、以降は再利用）
chrome-debug() {
  local dst="$HOME/.chrome-automation-profile"

  if pgrep -x "Google Chrome" > /dev/null; then
    echo "Chromeを終了中..."
    osascript -e 'quit app "Google Chrome"'
    sleep 2
  fi

  # 初回のみプロファイルをコピー
  if [ ! -d "$dst" ]; then
    echo "初回セットアップ: プロファイルをコピー中..."
    ditto "$HOME/Library/Application Support/Google/Chrome" "$dst"
    echo "セットアップ完了"
  fi

  echo "CDP起動中 (port: 9222) | プロファイル: $dst"

  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --user-data-dir="$dst" \
    --no-first-run \
    "$@"
}
```

設定を反映:
```bash
source ~/.zshrc
```

---

## 4. 使い方

### Chrome を CDP モードで起動（別ターミナルで実行）

```bash
chrome-debug
```

このターミナルは **開いたままにしておく**。

### agent-browser で接続

```bash
# 接続テスト
agent-browser --cdp 9222 get url

# ページを開く
agent-browser --cdp 9222 open https://example.com

# スナップショット取得
agent-browser --cdp 9222 snapshot -i -c
```

---

## 5. トラブルシューティング

### 接続できない場合

```bash
# CDP ポートが開いているか確認
curl -s http://localhost:9222/json/version

# Chrome プロセスを確認
ps aux | grep "Google Chrome" | grep remote-debugging
```

### プロファイルを更新したい場合

既存のプロファイルから最新の認証情報をコピーし直す:

```bash
# 既存の専用プロファイルを削除
rm -rf "$HOME/.chrome-automation-profile"

# 次回 chrome-debug 実行時に自動的に再コピーされる
```

---

## 参考リンク

- agent-browser 公式: https://github.com/vercel-labs/agent-browser
- agent-browser ドキュメント: https://agent-browser.dev/
- Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/

# agent-browser セットアップガイド

Chrome 144+ の `chrome://inspect/#remote-debugging` を使い、普段使いの Chrome にそのまま CDP 接続する方式です。
専用プロファイルや Chrome の再起動は不要です。

## 1. agent-browser のインストール

公式: https://github.com/vercel-labs/agent-browser

```bash
npm install -g agent-browser
```

インストール確認:
```bash
agent-browser --version
```

**v0.9.0 以上が必要です**（`--cdp` に WebSocket URL を渡す機能が必要）。

---

## 2. Chrome でリモートデバッグを有効化

Chrome で以下の URL を開く:

```
chrome://inspect/#remote-debugging
```

「Allow remote debugging for this browser instance」のチェックボックスをオンにする。
`Server running at: 127.0.0.1:9222` と表示されれば成功。

> **注意**: Chrome を再起動するとリモートデバッグは無効に戻ります。再度有効化が必要です。

---

## 3. シェルヘルパーの設定

`.zshrc` または `.bashrc` に以下を追加します。

**エイリアス名の確認**: 以下では `ab` をエイリアス名として使います。既に `ab` を別の用途で使っている場合は、別の名前（例: `abr`）に変更してください。

```bash
# agent-browser CDP helper (Chrome 144+ chrome://inspect/#remote-debugging 方式)
cdp-url() {
  local port_file="$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
  if [ ! -f "$port_file" ]; then
    echo "Error: DevToolsActivePort not found. Enable remote debugging at chrome://inspect/#remote-debugging" >&2
    return 1
  fi
  local port=$(sed -n '1p' "$port_file")
  local path=$(sed -n '2p' "$port_file")
  echo "ws://127.0.0.1:${port}${path}"
}

ab() {
  local ws_url
  ws_url=$(cdp-url) || return 1
  agent-browser --cdp "$ws_url" "$@"
}
```

設定を反映:
```bash
source ~/.zshrc
```

---

## 4. 動作確認

```bash
# 接続テスト
ab get url

# スナップショット
ab snapshot -i -c
```

---

## 5. トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `DevToolsActivePort not found` | Chrome で `chrome://inspect/#remote-debugging` を開いてリモートデバッグを有効化 |
| `Failed to connect via CDP` | Chrome が起動しているか確認。リモートデバッグが有効か確認 |
| Chrome 再起動後に接続できない | リモートデバッグは Chrome 再起動で無効に戻る。再度有効化が必要 |
| ref が見つからない | `ab snapshot -i -c` を再実行 |

### DevToolsActivePort の確認

```bash
# ファイルの存在確認
cat "$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"

# WebSocket URL の確認
cdp-url
```

---

## 参考リンク

- agent-browser 公式: https://github.com/vercel-labs/agent-browser
- Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/
- Chrome リモートデバッグのセキュリティ変更: https://developer.chrome.com/blog/remote-debugging-port

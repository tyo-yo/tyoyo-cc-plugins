---
name: agent-browser
description: This skill should be used when the user asks to "automate browser", "scrape website", "take screenshot of page", "fill form automatically", "click button on page", "interact with web page", "use agent-browser", "connect to Chrome with CDP", "browser automation", or needs to control a web browser programmatically for testing, scraping, or automation tasks.
allowed-tools: Bash(agent-browser:*), Bash(ab:*), Bash(ab *), Bash(cdp-url)
---

# agent-browser - Browser Automation CLI

公式: https://github.com/vercel-labs/agent-browser

**前提**: Chrome で `chrome://inspect/#remote-debugging` のリモートデバッグが有効であること。

## CDP 接続確認

```bash
ab get url
```

**接続失敗時**: ユーザーに Chrome で `chrome://inspect/#remote-debugging` を開いてリモートデバッグを有効化してもらう。
セットアップが必要な場合は `SETUP.md` を参照。セットアップの中で `ab` というエイリアス名を使うが、ユーザーに `ab` で良いか確認してから進めること。

---

## 基本ワークフロー

```bash
# 1. ページを開く
ab open https://example.com

# 2. インタラクティブ要素を取得（-c で空要素を除去）
ab snapshot -i -c

# 3. 要素を操作（@e1, @e2 などの ref を使用）
ab click @e3
ab fill @e5 "text"

# 4. ページ変更後は必ず再snapshot
ab snapshot -i -c
```

**重要**: クリック、入力、ナビゲーション後は必ず `snapshot` を再実行。DOM変更で ref が無効になる。

---

## 主要コマンド

### ナビゲーション
```bash
ab open <url>       # URL を開く
ab back             # 戻る
ab forward          # 進む
ab reload           # リロード
```

### スナップショット（AI にとって最重要）
```bash
ab snapshot -i      # インタラクティブ要素のみ
ab snapshot -i -c   # コンパクト表示（推奨）
ab snapshot -d 5    # 深度制限
ab snapshot -s "form"  # セレクタでスコープ
```

### インタラクション
```bash
ab click @e1        # クリック
ab fill @e2 "text"  # クリア＆入力
ab type @e2 "text"  # 追記入力
ab press Enter      # キー押下
ab select @e3 "option"  # ドロップダウン
ab check @e4        # チェックボックス
ab scroll down 500  # スクロール
```

### 情報取得
```bash
ab get text @e1     # テキスト
ab get html @e1     # HTML
ab get value @e1    # input の value
ab get url          # 現在の URL
ab get title        # ページタイトル
```

### スクリーンショット
```bash
ab screenshot              # 表示領域
ab screenshot -f           # 全体
ab screenshot output.png   # パス指定
ab pdf output.pdf          # PDF保存
```

### タブ操作
```bash
ab tab list         # タブ一覧
ab tab new          # 新規タブ
ab tab close        # タブを閉じる
```

---

## 待機・状態確認

```bash
ab wait @e1         # 要素の出現を待つ
ab wait 2000        # ミリ秒待機
ab is visible @e1   # 表示確認
ab is enabled @e1   # 有効確認
```

---

## セマンティックロケーター

ref が見つからない場合:

```bash
ab find role button click --name "Submit"
ab find text "ログイン" click
ab find label "メールアドレス" fill "user@example.com"
```

---

## よくあるパターン

### フォーム送信
```bash
ab open https://example.com/login
ab snapshot -i -c
ab fill @e3 "username"
ab fill @e4 "password"
ab click @e5
ab wait 2000
ab snapshot -i -c
```

### データ抽出
```bash
ab open https://example.com/data
ab snapshot -i -c
ab get text @e1
ab get html ".data-table"
```

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `DevToolsActivePort not found` | Chrome で `chrome://inspect/#remote-debugging` を開いてリモートデバッグを有効化 |
| `Failed to connect via CDP` | Chrome が起動しているか確認。リモートデバッグが有効か確認 |
| ref が見つからない | `ab snapshot -i -c` を再実行 |
| クリックが効かない | `ab wait @e1` で待機してから実行 |
| ページ遷移後にエラー | `ab snapshot` を再実行して新しい ref を取得 |
| ダウンロードしたファイルが見つからない | CDP モードでは `/var/folders/.../playwright-artifacts-*/` に保存される場合がある。`find /var/folders -name "ファイル名の一部" 2>/dev/null` で検索 |

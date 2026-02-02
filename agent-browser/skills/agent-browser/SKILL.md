---
name: agent-browser
description: This skill should be used when the user asks to "automate browser", "scrape website", "take screenshot of page", "fill form automatically", "click button on page", "interact with web page", "use agent-browser", "connect to Chrome with CDP", "browser automation", or needs to control a web browser programmatically for testing, scraping, or automation tasks.
allowed-tools: Bash(agent-browser:*)
---

# agent-browser - Browser Automation CLI

公式: https://github.com/vercel-labs/agent-browser

**前提**: `chrome-debug` コマンドで Chrome が CDP モードで起動済みであること。

## CDP 接続確認

```bash
# 接続テスト
agent-browser --cdp 9222 get url
```

**接続失敗時**: ユーザーに別ターミナルで `chrome-debug` を実行してもらう。
セットアップが必要な場合は `SETUP.md` を参照。

---

## 基本ワークフロー

```bash
# 1. ページを開く
agent-browser --cdp 9222 open https://example.com

# 2. インタラクティブ要素を取得（-c で空要素を除去）
agent-browser --cdp 9222 snapshot -i -c

# 3. 要素を操作（@e1, @e2 などの ref を使用）
agent-browser --cdp 9222 click @e3
agent-browser --cdp 9222 fill @e5 "text"

# 4. ページ変更後は必ず再snapshot
agent-browser --cdp 9222 snapshot -i -c
```

**重要**: クリック、入力、ナビゲーション後は必ず `snapshot` を再実行。DOM変更で ref が無効になる。

---

## 主要コマンド

### ナビゲーション
```bash
agent-browser --cdp 9222 open <url>       # URL を開く
agent-browser --cdp 9222 back             # 戻る
agent-browser --cdp 9222 forward          # 進む
agent-browser --cdp 9222 reload           # リロード
```

### スナップショット（AI にとって最重要）
```bash
agent-browser --cdp 9222 snapshot -i      # インタラクティブ要素のみ
agent-browser --cdp 9222 snapshot -i -c   # コンパクト表示（推奨）
agent-browser --cdp 9222 snapshot -d 5    # 深度制限
agent-browser --cdp 9222 snapshot -s "form"  # セレクタでスコープ
```

### インタラクション
```bash
agent-browser --cdp 9222 click @e1        # クリック
agent-browser --cdp 9222 fill @e2 "text"  # クリア＆入力
agent-browser --cdp 9222 type @e2 "text"  # 追記入力
agent-browser --cdp 9222 press Enter      # キー押下
agent-browser --cdp 9222 select @e3 "option"  # ドロップダウン
agent-browser --cdp 9222 check @e4        # チェックボックス
agent-browser --cdp 9222 scroll down 500  # スクロール
```

### 情報取得
```bash
agent-browser --cdp 9222 get text @e1     # テキスト
agent-browser --cdp 9222 get html @e1     # HTML
agent-browser --cdp 9222 get value @e1    # input の value
agent-browser --cdp 9222 get url          # 現在の URL
agent-browser --cdp 9222 get title        # ページタイトル
```

### スクリーンショット
```bash
agent-browser --cdp 9222 screenshot              # 表示領域
agent-browser --cdp 9222 screenshot -f           # 全体
agent-browser --cdp 9222 screenshot output.png   # パス指定
agent-browser --cdp 9222 pdf output.pdf          # PDF保存
```

### タブ操作
```bash
agent-browser --cdp 9222 tab list         # タブ一覧
agent-browser --cdp 9222 tab new          # 新規タブ
agent-browser --cdp 9222 tab close        # タブを閉じる
```

---

## 待機・状態確認

```bash
agent-browser --cdp 9222 wait @e1         # 要素の出現を待つ
agent-browser --cdp 9222 wait 2000        # ミリ秒待機
agent-browser --cdp 9222 is visible @e1   # 表示確認
agent-browser --cdp 9222 is enabled @e1   # 有効確認
```

---

## セマンティックロケーター

ref が見つからない場合:

```bash
agent-browser --cdp 9222 find role button click --name "Submit"
agent-browser --cdp 9222 find text "ログイン" click
agent-browser --cdp 9222 find label "メールアドレス" fill "user@example.com"
```

---

## よくあるパターン

### フォーム送信
```bash
agent-browser --cdp 9222 open https://example.com/login
agent-browser --cdp 9222 snapshot -i -c
agent-browser --cdp 9222 fill @e3 "username"
agent-browser --cdp 9222 fill @e4 "password"
agent-browser --cdp 9222 click @e5
agent-browser --cdp 9222 wait 2000
agent-browser --cdp 9222 snapshot -i -c
```

### データ抽出
```bash
agent-browser --cdp 9222 open https://example.com/data
agent-browser --cdp 9222 snapshot -i -c
agent-browser --cdp 9222 get text @e1
agent-browser --cdp 9222 get html ".data-table"
```

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `Failed to connect via CDP` | `chrome-debug` を別ターミナルで実行 |
| ref が見つからない | `snapshot -i -c` を再実行 |
| クリックが効かない | `wait @e1` で待機してから実行 |
| ページ遷移後にエラー | `snapshot` を再実行して新しい ref を取得 |

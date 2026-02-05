---
name: mcpc
description: |
  Use this skill when the user needs to pipe file contents to MCP tools, batch-call MCP tools,
  filter or grep long MCP output, or use mcpc for efficient MCP operations that bypass LLM context.
  Use when user asks to "use mcpc", "pipe to MCP", "mcpc call", "MCP output is too long",
  "batch MCP operations", "upload file to Notion via CLI", "call MCP tool from bash",
  "send file to MCP without reading it", or needs to process MCP tool results with jq/grep/head.
---

# mcpc - MCP ツールを Unix パイプで操作する

mcpc は MCP サーバーのツールを CLI から直接呼び出すクライアント。LLM のコンテキストを通さずに、ファイル入力やパイプ処理で MCP ツールを操作できる。

**前提**: `mcpc` がインストール済みで、対象サーバーに認証済みであること。未セットアップの場合は `SETUP.md` を参照。

---

## いつ mcpc を使うか

以下のケースでは mcpc を Bash で実行する方が通常の MCP ツール呼び出しより効率的:

| ケース | 理由 |
|--------|------|
| ファイルの中身を MCP ツールに送る | ファイル内容が LLM コンテキストを2回通過（Read + ツール呼び出し）するのを回避 |
| MCP 出力が長く、一部だけ必要 | jq/grep/head でフィルタしてから結果を確認できる |
| 同じツールをバッチで複数回呼ぶ | ループで効率的に処理 |

**通常の MCP ツール呼び出しで十分な場合（短い入出力、1回の呼び出し）は mcpc を使わない。**

---

## 基本構文

```bash
# ツール一覧
mcpc <server-url> tools-list

# ツール詳細（引数スキーマ確認）
mcpc <server-url> tools-get <tool-name>

# ツール呼び出し（引数を直接指定）
mcpc <server-url> tools-call <tool-name> key1:="value1" key2:=123

# ツール呼び出し（JSON で引数指定）
mcpc <server-url> tools-call <tool-name> '{"key1": "value1", "key2": 123}'

# ツール呼び出し（stdin からパイプ）
echo '{"key": "value"}' | mcpc <server-url> tools-call <tool-name>

# JSON 出力（パイプ・スクリプト用）
mcpc <server-url> tools-call <tool-name> '{"key": "value"}' --json
```

**`:=` 構文の注意**: キーと値の間にスペースを入れない。`key:="value"` は OK、`key :="value"` は NG。

**`--config` フラグ**: 既存の `.mcp.json` ファイルからサーバー設定を読み込める:

```bash
mcpc --config .mcp.json <server-name> tools-list
```

**よく使うサーバー URL:**
- Notion: `https://mcp.notion.com/mcp`

---

## コアパターン

### パターン 1: ファイル → MCP ツール（LLM バイパス）

マークダウンファイルを Notion ページとしてアップロード:

```bash
FILE="/path/to/document.md"
PARENT_PAGE_ID="xxxxxxxx"

jq -n \
  --arg title "$(basename "$FILE" .md)" \
  --arg content "$(cat "$FILE")" \
  --arg parent "$PARENT_PAGE_ID" \
  '{parent:{page_id:$parent},pages:[{properties:{title:$title},content:$content}]}' \
| mcpc https://mcp.notion.com/mcp tools-call notion-create-pages --json
```

### パターン 2: 長い出力のフィルタリング

Notion 検索結果からタイトルだけ抽出:

```bash
mcpc https://mcp.notion.com/mcp tools-call notion-search '{"query":"議事録"}' --json \
  | jq -r '.content[0].text' | jq -r '.results[] | .title'
```

出力の先頭 N 行だけ確認:

```bash
mcpc <url> tools-call <tool> '{"query":"keyword"}' --json | head -50
```

### パターン 3: バッチ処理（JSONL → 複数回呼び出し）

JSONL ファイルの各行を MCP ツールに送る:

```bash
while IFS= read -r line; do
  title=$(echo "$line" | jq -r '.title')
  content=$(echo "$line" | jq -r '.content')
  jq -n --arg t "$title" --arg c "$content" --arg p "$PARENT_ID" \
    '{parent:{page_id:$p},pages:[{properties:{title:$t},content:$c}]}' \
  | mcpc https://mcp.notion.com/mcp tools-call notion-create-pages --json
done < records.jsonl
```

### パターン 4: 結果をファイルに保存

```bash
mcpc <url> tools-call <tool> '{"query":"data"}' --json > /tmp/result.json
# 結果を Read ツールで確認、または jq で加工
jq '.content[0].text | fromjson' /tmp/result.json
```

### パターン 5: 持続セッション（バッチ処理の高速化）

通常 mcpc は呼び出しごとに接続を開閉する。バッチ処理で複数回呼ぶ場合はセッションを維持すると高速:

```bash
# セッションを開始（バックグラウンドで接続維持）
mcpc https://mcp.notion.com/mcp connect @notion

# セッション経由でツール呼び出し（接続済みなので高速）
mcpc @notion tools-call notion-search '{"query":"keyword"}' --json
mcpc @notion tools-call notion-fetch '{"id":"page-id"}' --json

# セッションを閉じる
mcpc @notion close
```

`@session-name` はローカルのセッション識別子。任意の名前を付けられる。

---

## `--json` 出力の構造

mcpc の `--json` 出力は MCP プロトコルの標準形式:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"actual_result\": \"here\"}"
    }
  ]
}
```

実際のデータは `.content[0].text` に JSON 文字列として格納される。二重パースが必要:

```bash
mcpc <url> tools-call <tool> '...' --json \
  | jq -r '.content[0].text' | jq '.'
```

---

## 注意事項

- mcpc は各呼び出しで HTTP 接続を行う。バッチ処理では `connect @session` で接続を維持する（パターン 5 参照）
- OAuth トークンは OS キーチェーンに保存される。期限切れ時は `mcpc <url> login` で再認証
- `--json` を付けないと人間向けのフォーマットで出力される。パイプ処理時は必ず `--json` を付ける
- `--json` モードではエラーは stderr に出力される。パイプ先にはツール結果のみ流れるため安全
- 終了コード: `0`=成功、`1`=クライアントエラー、`2`=サーバーエラー、`3`=ネットワークエラー、`4`=認証エラー。スクリプトで `$?` をチェックしてエラーハンドリングに使える

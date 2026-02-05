# mcpc

MCP ツールを Unix パイプで操作するスキル。

[mcpc](https://github.com/apify/mcp-cli) (Apify 製 MCP CLI クライアント) を使って、ファイル入力からの MCP ツール呼び出しや、長い出力のフィルタリングを LLM コンテキストを通さずに実行する。

## ユースケース

- マークダウンファイルを Notion ページとしてアップロード
- MCP ツールの出力を jq/grep でフィルタ
- JSONL ファイルからバッチで MCP ツールを呼び出し

## セットアップ

```bash
npm install -g @apify/mcpc
mcpc https://mcp.notion.com/mcp login
```

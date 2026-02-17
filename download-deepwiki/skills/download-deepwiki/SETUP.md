# Setup: download-deepwiki

## 前提条件

### 1. mcpc のインストール

```bash
npm install -g mcpc
# または
bun install -g mcpc
```

インストール確認:
```bash
mcpc --version
```

### 2. Devin API キーの取得

1. [https://app.devin.ai/](https://app.devin.ai/) にアクセスしてログイン
2. Settings → API Keys からキーを生成
3. リポジトリを登録（未登録の場合は "Add Repository" から追加）

### 3. 環境変数の設定

```bash
export DEVIN_API_KEY=your_api_key_here
```

恒久化するには `~/.zshrc` または `~/.bashrc` に追加:

```bash
echo 'export DEVIN_API_KEY=your_api_key_here' >> ~/.zshrc
```

### 4. プロジェクトの .mcp.json 設定

プロジェクトルートに `.mcp.json` を作成または追記:

```json
{
  "mcpServers": {
    "private-deepwiki": {
      "type": "http",
      "url": "https://mcp.devin.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${DEVIN_API_KEY}"
      }
    }
  }
}
```

`${DEVIN_API_KEY}` は mcpc が実行時に環境変数から自動展開する。

---

## 動作確認

セットアップ後、以下で動作を確認:

```bash
# ウィキ構造の取得テスト
mcpc --config .mcp.json private-deepwiki tools-call read_wiki_structure \
  '{"repoName":"owner/repo"}' --json | head -20
```

正常なら `{"content":[{"type":"text","text":"Available pages for ..."}]}` のようなJSONが返る。

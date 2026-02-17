---
name: download-deepwiki
description: |
  DeepWiki（private-deepwiki MCP）のコンテンツをローカルにダウンロードして
  階層構造のマークダウンとして保存するスキル。
  "DeepWikiをダウンロード", "download deepwiki", "DeepWikiを保存", "DeepWikiを同期",
  "sync deepwiki", "wiki content をローカルに保存", ".kiro/deepwiki に保存"
  のような指示で使用する。mcpc と private-deepwiki MCP サーバーを使用する。
allowed-tools: Bash(command:uv run *), Bash(command:mcpc *), Bash(command:chmod *)
---

# DeepWiki ダウンローダー

private-deepwiki MCP サーバーから Wiki コンテンツを取得し、ウィキの番号階層に沿った
ディレクトリ構造のマークダウンとして `.kiro/deepwiki/` に保存するスキル。
セットアップ要件は `SETUP.md` を参照。

---

## 前提確認

実行前に以下を確認する:

1. `mcpc` がインストール済みか確認する
2. プロジェクトルートに `.mcp.json` があり `private-deepwiki` サーバーが設定されているか確認する
3. `DEVIN_API_KEY` 環境変数が設定されているか確認する

不足がある場合は `SETUP.md` に従ってセットアップを促す。

---

## 実行手順

### Step 1: リポジトリ名を特定する

ユーザーの指示や現在のリポジトリから `owner/repo` 形式のリポジトリ名を特定する。
明示されていない場合は `git remote get-url origin` で確認する。

### Step 2: スクリプトを実行する

プラグインに含まれるスクリプトをプロジェクトルートから実行する:

```bash
uv run $CLAUDE_PLUGIN_ROOT/scripts/download_deepwiki.py \
  --repo <owner/repo> \
  [--output-dir <path>]   # 省略時: .kiro/deepwiki
  [--mcp-config <path>]   # 省略時: .mcp.json (CWD)
  [--server <name>]       # 省略時: private-deepwiki
  [--no-clean]            # 既存ファイルを保持して差分更新
```

**例（elyza_llm_apps の場合）:**

```bash
uv run $CLAUDE_PLUGIN_ROOT/scripts/download_deepwiki.py \
  --repo elyza-inc/elyza_llm_apps
```

### Step 3: 出力を確認する

スクリプトは以下の出力を行う:

```
Repo   : elyza-inc/elyza_llm_apps
Output : /path/to/project/.kiro/deepwiki

[1/3] Fetching wiki structure...
       52 pages found
[2/3] Fetching wiki contents...
       52 pages fetched
[3/3] Saving pages...
       01_Overview.md
       04_Applications/index.md
       04_Applications/4.1_Simple_App.md
       04_Applications/4.2_System_App/index.md
       ...

Done! 52 pages saved to .kiro/deepwiki
```

---

## 保存されるディレクトリ構造

ウィキの番号階層がそのままディレクトリ構造に反映される:

```
.kiro/deepwiki/
├── 01_Overview.md
├── 02_Getting_Started.md
├── 04_Applications/
│   ├── index.md                  ← "4 Applications" 本体
│   ├── 4.1_Simple_App.md
│   ├── 4.2_System_App/
│   │   ├── index.md              ← "4.2 System App" 本体
│   │   ├── 4.2.1_Workflow.md
│   │   └── ...
│   └── ...
├── 05_LLM_Provider_Integration/
│   └── ...
└── ...
```

- **子を持つセクション**: ディレクトリになり、自身の内容は `index.md` として保存
- **末端セクション**: 親ディレクトリ直下の `.md` ファイルとして保存

---

## 定期更新

DeepWiki は定期的に更新されるため、以下のコマンドで最新化できる:

```bash
# クリーン更新（デフォルト: 既存を削除して全ページ再取得）
uv run $CLAUDE_PLUGIN_ROOT/scripts/download_deepwiki.py --repo <owner/repo>

# 差分更新（既存ファイルを保持して上書き）
uv run $CLAUDE_PLUGIN_ROOT/scripts/download_deepwiki.py --repo <owner/repo> --no-clean
```

---

## トラブルシューティング

| エラー | 原因 | 対処 |
|--------|------|------|
| `mcpc: command not found` | mcpc 未インストール | `SETUP.md` 参照 |
| `401 Unauthorized` | DEVIN_API_KEY 未設定または期限切れ | `export DEVIN_API_KEY=...` または再認証 |
| `Repository not found` | リポジトリ名が間違っている | `owner/repo` 形式を確認 |
| `JSONDecodeError` | mcpc 出力が壊れている | `--json` フラグの挙動を確認、再試行 |

# download-deepwiki

DeepWiki（private-deepwiki MCP）のコンテンツを mcpc 経由で取得し、
ウィキの番号階層を保ったままローカルのマークダウンファイルとして保存するプラグイン。

## 機能

- ウィキ構造を自動解析して階層ディレクトリを構築
- 子を持つセクションはディレクトリ + `index.md`、末端セクションは `.md` ファイルに保存
- `--no-clean` オプションで差分更新に対応
- `--repo` / `--output-dir` / `--mcp-config` / `--server` で柔軟に設定可能

## 使い方

"DeepWikiをダウンロード" や "sync deepwiki" と指示すると自動でスキルが読み込まれる。

または直接実行:

```bash
uv run $CLAUDE_PLUGIN_ROOT/scripts/download_deepwiki.py --repo owner/repo
```

## 前提条件

- `mcpc` CLI のインストール
- `DEVIN_API_KEY` 環境変数
- `.mcp.json` に `private-deepwiki` サーバーの設定

詳細は `skills/download-deepwiki/SETUP.md` を参照。

## ファイル構成

```
download-deepwiki/
├── .claude-plugin/
│   └── plugin.json
├── skills/download-deepwiki/
│   ├── SKILL.md      # Claude へのガイド
│   └── SETUP.md      # セットアップ手順
├── scripts/
│   └── download_deepwiki.py  # 実行スクリプト（uv run 対応）
└── README.md
```

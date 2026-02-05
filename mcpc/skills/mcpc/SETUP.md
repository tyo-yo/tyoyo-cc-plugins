# mcpc セットアップガイド

初回のみ必要な作業。

## 1. mcpc のインストール

```bash
npm install -g @apify/mcpc
```

インストール確認:
```bash
mcpc --version
```

---

## 2. MCP サーバーへの認証

mcpc は OAuth 2.0 で認証する。各サーバーに対して初回のみブラウザ認証が必要。

### Notion

```bash
mcpc https://mcp.notion.com/mcp login
# ブラウザが開く → Notion で「アクセスを許可」→ 完了
```

### その他のサーバー

```bash
mcpc <server-url> login
```

認証済みプロファイルの確認:
```bash
mcpc  # 引数なしで、セッション・プロファイル一覧を表示
```

---

## 3. 接続確認

```bash
# ツール一覧が表示されれば OK
mcpc https://mcp.notion.com/mcp tools-list
```

---

## 4. トラブルシューティング

### 404 Not Found

サーバー URL の末尾にパスが必要な場合がある:
- `mcp.notion.com` → `https://mcp.notion.com/mcp`

### 認証期限切れ

```bash
mcpc <server-url> login
```

で再認証。

### キャッシュ・セッションのクリーンアップ

動作がおかしい場合、ローカルデータをリセット:
```bash
mcpc --clean
```

### libsecret エラー (Linux)

mcpc は OS キーチェーンにトークンを保存する。Linux では:
```bash
sudo apt install libsecret-1-dev
```

---

## 5. Bearer トークン認証（OAuth の代替）

OAuth が使えない環境では、Bearer トークンで直接認証も可能:

```bash
mcpc <server-url> --bearer-token "<token>" tools-list
```

環境変数でも指定可能（スクリプト向け）。通常は OAuth で十分。

---

## 参考リンク

- mcpc 公式: https://github.com/apify/mcp-cli
- mcpc ドキュメント: https://raw.githubusercontent.com/apify/mcpc/main/README.md

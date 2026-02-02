---
name: gogcli
description: Google Workspace CLI (gogcli) for Gmail, Calendar, Drive, Tasks. Use when user wants to check emails, view calendar events, manage Drive files, or work with tasks.
allowed-tools: Bash(gog:*)
---

# gogcli - Google Workspace CLI

公式: https://github.com/shinichi-kogiso/gogcli

## 認証（初回のみ）

```bash
gog auth add <email>      # アカウント追加（ブラウザ認証）
gog auth list             # 認証済みアカウント一覧
gog auth status           # 認証状態確認
```

## 共通フラグ

| フラグ | 説明 |
|--------|------|
| `--json` | JSON出力 |
| `--account <email>` | アカウント指定 |
| `--max <n>` | 結果数制限 |

---

## Gmail (`gog gmail`)

```bash
gog gmail search "<query>"      # 検索（スレッド単位）
gog gmail get <messageId>       # メッセージ取得
gog gmail send --to "..." --subject "..." --body "..."  # 送信
gog gmail labels list           # ラベル一覧
```

**検索演算子**: `from:`, `to:`, `subject:`, `is:unread`, `has:attachment`, `newer_than:1d`, `after:2024/01/01`, `in:inbox`

---

## Calendar (`gog calendar`)

```bash
gog calendar events             # 予定一覧（primaryカレンダー）
gog calendar events --today     # 今日の予定
gog calendar events --from "2024-01-01" --to "2024-01-31"
gog calendar create primary --summary "会議" --from "2024-01-15T10:00" --to "2024-01-15T11:00"
gog calendar delete primary <eventId>
```

**注意**: `events`はデフォルトで`primary`カレンダー。他のカレンダーは`gog calendar calendars`で確認。

### メンバー検索 & ミーティング設定

```bash
# 1. メンバーを検索（名前やメールで）
gog people search "yamada"

# 2. 複数人の空き状況を確認
gog calendar freebusy "user1@example.com,user2@example.com" --from "2024-01-15T10:00:00+09:00" --to "2024-01-15T17:00:00+09:00"

# 3. ミーティング作成（Google Meet付き）
gog calendar create primary --summary "会議" --from "2024-01-15T10:00:00+09:00" --to "2024-01-15T11:00:00+09:00" --attendees "user1@example.com,user2@example.com" --with-meet
```

**重要**:
- 時刻は必ずJST（`+09:00`）で指定する
- 営業時間は10:00-17:00を基本とする（18:00-19:00は避ける）
- ミーティング作成時は必ず`--with-meet`を付けてGoogle Meetリンクを生成する

---

## Drive (`gog drive`)

```bash
gog drive ls                    # ファイル一覧（ルート）
gog drive ls <folderId>         # フォルダ内一覧
gog drive search "keyword"      # 検索
gog drive download <fileId>     # ダウンロード
gog drive upload /path/to/file  # アップロード
gog drive mkdir "フォルダ名"    # フォルダ作成
gog drive delete <fileId>       # 削除（ゴミ箱へ）
gog drive share <fileId> --email "user@example.com" --role reader
```

**注意**: `list`ではなく`ls`。

---

## Tasks (`gog tasks`)

```bash
gog tasks lists list            # タスクリスト一覧（IDを確認）
gog tasks list <tasklistId>     # タスク一覧
gog tasks add <tasklistId> --title "タスク名" --due "2024-01-15"
gog tasks done <tasklistId> <taskId>    # 完了
gog tasks delete <tasklistId> <taskId>  # 削除
```

**重要**: ほぼ全てのコマンドで`<tasklistId>`が必須。まず`gog tasks lists list`でIDを確認すること。

---

## トラブルシューティング

```bash
gog <command> --help    # 各コマンドのヘルプ
gog auth status         # 認証状態確認
```

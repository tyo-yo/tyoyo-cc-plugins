# ccbut-auto-commit

Claude Code の Stop フックプラグイン。セッション終了時に、GitButler (`but` コマンド) を使って変更を自動コミットします。

## 機能

- セッション中に Edit/Write ツールで変更されたファイルのみを検出しコミット
- GitButler のブランチ管理と連携（ファイルの自動割り当て）
- Claude Haiku でコミットタイトルを自動生成（Conventional Commits 形式）
- 環境変数による柔軟な設定

## 前提条件

- [Bun](https://bun.sh/) がインストールされていること
- [GitButler CLI](https://gitbutler.com/) (`but` コマンド) がインストールされていること
- Claude Code CLI (`claude` コマンド) がインストールされていること（タイトル生成用）

## インストール

Claude Code の設定でプラグインを有効化してください。

## 環境変数

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| `CCBUT_BRANCH` | (未設定) | コミット先ブランチ名。**未設定の場合はスキップ** |
| `CCBUT_MESSAGE_MAX_LENGTH` | `2000` | タイトル生成に使うメッセージ最大長 |
| `CCBUT_TITLE_PROMPT` | (日本語プロンプト) | コミットタイトル生成プロンプト |
| `CCBUT_COMMIT_FOOTER` | (自動生成フッター) | コミットメッセージのフッター |
| `CCBUT_LOG_FILE` | `/tmp/ccbut-auto-commit.log` | ログファイルパス |

## 使い方

`CCBUT_BRANCH` 環境変数を設定した状態で Claude Code を使うと、セッション終了時に自動コミットされます。

```bash
CCBUT_BRANCH=my-feature claude
```

## 仕組み

1. Claude Code セッションが終了すると Stop フックが発火
2. トランスクリプトから Edit/Write ツールで変更されたファイルと最後のメッセージを抽出
3. `git status` の変更ファイルとセッション中の編集ファイルを照合
4. `CCBUT_BRANCH` で指定されたブランチにファイルを割り当て
5. Claude Haiku でコミットタイトルを生成し、`but commit` でコミット

## ログ

デバッグ用ログは `/tmp/ccbut-auto-commit.log`（または `CCBUT_LOG_FILE` で指定したパス）に出力されます。

---
name: refactor-test-agent
description: Refactor given test files using steering + refactor-test-rules — one pass, returns undone candidates
tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep
model: inherit
color: blue
---

# refactor-test-agent

与えられたテストファイルリストを1パスリファクタリングする。spec は読まない。

## 入力

- 対象テストファイルリスト（コマンド側が決定済み）
- パス番号
- 前パスの未対応候補（スキップ対象）

## Step 1: ルール読み込み

- `${CLAUDE_PLUGIN_ROOT}/skills/kirox/references/refactor-test-rules.md`
- `.kiro/steering/*.md`（特に重視）

## Step 2: 参照実装の探索

対象ファイルと同レイヤー・同ライブラリを使う、現在変更中でないテストファイルを3つ以上読む（既存パターン把握のため）。

## Step 3: リファクタリング

各対象ファイルにルールのチェックリストを適用。変更後にテストを実行し、グリーン維持できない変更は revert して未対応候補へ。前パスの未対応候補は再試行せずスキップ。

**変えてよい**: 命名、重複フィクスチャ整理、アサーション明確化、未使用インポート削除
**変えてはいけない**: テスト対象の挙動、モック構造、テストの独立性

## 出力

変更内容サマリーと `## 未対応候補` セクション（ファイル:行 + 理由）

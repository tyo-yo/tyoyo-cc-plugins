---
description: Run REFACTOR phase for test code — 3 sequential passes then interactive review
allowed-tools: Read, Bash, Task
argument-hint: "[feature-name] [task-numbers]"
---

# spec-refactor-test

## 対象ファイルの決定

1. ブランチ名から feature を推測: `git rev-parse --abbrev-ref HEAD`（引数があれば優先）
2. `.kiro/specs/{feature}/tasks.md` からテストファイルを抽出（存在する場合）
3. `git log --name-only -10` で直近の変更ファイルとコミットメッセージを確認
4. 上記を合わせてリファクタリング対象の **テストファイルリスト** を確定し、ユーザーに明示

## 3パス実行

refactor-test-agent を3回直列で呼び出す。各パスの出力はそのまま表示する。

渡す情報: 対象ファイルリスト・パス番号（1/3, 2/3, 3/3）・前パスの未対応候補（パス1は空）

## 完了後

3パス分の未対応候補を重複排除してまとめ提示 → 1件ずつ対話的に解決。

承認された決定は `/Users/tyoyo/repos/tyoyo-cc-plugins/kirox/skills/kirox/references/refactor-test-rules.md` に追記する。

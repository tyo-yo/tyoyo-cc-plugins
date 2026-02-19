---
description: Run REFACTOR phase for test code — 3 sequential passes then interactive review
allowed-tools: Read, Bash, Task
argument-hint: "[feature-name] [task-numbers]"
---

# spec-refactor-test

GREEN（テスト通過）後のテストコードのリファクタリングフェーズを実行する。
refactor-test-agent を3回直列で実行し、自動対応できなかった候補をまとめてインタラクティブに解決する。

## 引数パース

- `$1`: feature 名（省略可）
- `$2`: タスク番号（省略可、"1.1" or "1,2,3" 形式）

**厳密にパースできない場合の推測手順:**
1. `git rev-parse --abbrev-ref HEAD` でブランチ名を取得（Bash ツール使用）
2. `work/xxx`, `feature/xxx`, `feat/xxx` 等のパターンから feature 名を抽出
3. 推測した値をユーザーに明示して続行（確認は求めない）
4. `.kiro/specs/` に該当ディレクトリがなければ spec なしで続行（git diff のみで判断）

## 実行: 3パス直列

各パスで refactor-test-agent を呼び出す。前のパスの「自動対応できなかった候補」を次のパスに引き継ぐ。

### パス 1

```
Task(
  subagent_type="refactor-test-agent",
  prompt="""
Feature: {feature}
Spec directory: .kiro/specs/{feature}/  (存在する場合のみ参照)
Target tasks: {task numbers or "recent changes via git diff"}
Pass: 1/3
Previous candidates: (none)

File patterns to read:
- .kiro/specs/{feature}/*.{json,md}  (存在する場合)
- .kiro/steering/*.md
"""
)
```

パス1の出力から `## 自動対応できなかった候補` セクションを抽出する。

### パス 2

```
Task(
  subagent_type="refactor-test-agent",
  prompt="""
Pass: 2/3
Previous candidates from pass 1:
{pass1_candidates}

（その他は同じ）
"""
)
```

### パス 3

```
Task(
  subagent_type="refactor-test-agent",
  prompt="""
Pass: 3/3
Accumulated candidates from passes 1-2:
{pass1_candidates + pass2_candidates}

（その他は同じ）
"""
)
```

## 3パス完了後: まとめ提示

3パス分の候補を重複排除してまとめ、以下の形式でユーザーに提示する:

```
## テストリファクタリング候補（自動対応できなかった箇所）

1. `path/to/test_file.py:42` — {理由}
2. ...

順番に確認しますか？ (y でそのまま 1 件目へ / n でスキップ / done で終了)
```

## インタラクティブ解決

ユーザーと1件ずつ確認・修正を行う。各解決後:

「この決定を `${CLAUDE_PLUGIN_ROOT}/skills/kirox/references/refactor-test-rules.md` に追記して次回自動化しますか？」

ユーザーが承認した場合のみ追記する（追記後は tyoyo-cc-plugins リポジトリにコミットして蓄積する）。

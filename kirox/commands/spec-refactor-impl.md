---
description: Run REFACTOR phase for implementation code — 3 sequential passes then interactive review
allowed-tools: Read, Bash, Task
argument-hint: "[feature-name] [task-numbers]"
---

# spec-refactor-impl

GREEN（テスト通過）後の実装コードのリファクタリングフェーズを実行する。
refactor-impl-agent を3回直列で実行し、自動対応できなかった候補をまとめてインタラクティブに解決する。

## 引数パース

- `$1`: feature 名（省略可）
- `$2`: タスク番号（省略可、"1.1" or "1,2,3" 形式）

**厳密にパースできない場合の推測手順:**
1. `git rev-parse --abbrev-ref HEAD` でブランチ名を取得（Bash ツール使用）
2. `work/xxx`, `feature/xxx`, `feat/xxx` 等のパターンから feature 名を抽出
3. 推測した値をユーザーに明示して続行（確認は求めない）
4. `.kiro/specs/` に該当ディレクトリがなければ spec なしで続行（git diff のみで判断）

## 実行: 3パス直列

各パスで refactor-impl-agent を呼び出す。前のパスの「自動対応できなかった候補」を次のパスに引き継ぐ。

### パス 1

```
Task(
  subagent_type="refactor-impl-agent",
  prompt="""
Feature: {feature}
Spec directory: .kiro/specs/{feature}/  (存在する場合のみ参照)
Target tasks: {task numbers or "recent changes via git diff"}
Pass: 1/3
Previous candidates: (none)

File patterns to read:
- .kiro/specs/{feature}/*.{json,md}  (存在する場合)
- .kiro/steering/*.md
- .kirox/skills/references/refactor-impl-rules.md
"""
)
```

パス1の出力から `## 自動対応できなかった候補` セクションを抽出する。

### パス 2

```
Task(
  subagent_type="refactor-impl-agent",
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
  subagent_type="refactor-impl-agent",
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
## 実装リファクタリング候補（自動対応できなかった箇所）

1. `path/to/file.py:42` — {理由}
2. ...

順番に確認しますか？ (y でそのまま 1 件目へ / n でスキップ / done で終了)
```

## インタラクティブ解決

ユーザーと1件ずつ確認・修正を行う。各解決後:

「この決定を `.kirox/skills/references/refactor-impl-rules.md` に追記して次回自動化しますか？」

ユーザーが承認した場合のみ追記する。

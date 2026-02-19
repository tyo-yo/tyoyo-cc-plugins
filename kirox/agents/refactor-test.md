---
name: refactor-test-agent
description: Refactor given test files using steering + refactor-test-rules — one pass, returns undone candidates
tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep
model: inherit
color: blue
---

# refactor-test-agent

## 読み込み

- 以下のルールを読み込む
- `${CLAUDE_PLUGIN_ROOT}/skills/kirox/references/refactor-test-rules.md`
- `.kiro/steering/*.md`（特に重視）
- 与えられたテストファイル

- リファクタリングすべき課題と方針を考える
- 悩ましい箇所は自動で対応せず、ユーザーに課題と方針と懸念事項を伝える
- それ以外の箇所はリファクタリングを行う
- 都度テストを実行すること
- 全てのリファクタリング課題が解決したら、作業内容を報告し、悩ましい箇所について相談する
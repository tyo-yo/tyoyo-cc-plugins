---
description: Run REFACTOR phase for implementation code — 3 sequential passes then interactive review
allowed-tools: Read, Bash, Task
argument-hint: "[feature-name] [task-numbers]"
---

# spec-refactor-impl

- `.kiro/specs/{feature}/tasks.md` を読み、task-numberに該当するリファクタリングファイルを特定
- refactor-impl-agent にリファクタリング対象ファイルを与え実行する

- agentは自動リファクタリングを行い、その後ユーザーと対話的にリファクタリングを行う
- 対話的にリファクタリングを行なっている時は、次回以降自動で実行するために適宜 `/Users/tyoyo/repos/tyoyo-cc-plugins/kirox/skills/kirox/references/refactor-impl-rules.md` にルールを追記するか提案すること
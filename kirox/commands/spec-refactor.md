---
description: Run REFACTOR phase for test code — 3 sequential passes then interactive review
allowed-tools: Read, Bash, Task
argument-hint: "[mode] [feature-name] [task-numbers]"
---

# spec-refactor-test

- `.kiro/specs/{feature}/tasks.md` を読み、task-numberに該当するリファクタリングファイルを特定
- mode=testの場合テストファイルのみ、 mode=implの場合非テストファイルのみを対象とする
- refactor-impl-agent にリファクタリングで対象箇所（ファイル、差分、commit、関数など）を与え実行する
- agentは自動リファクタリングを行い、その後ユーザーと対話的にリファクタリングを行う
- 対話的にリファクタリングを行なっている時は、次回以降自動で実行するために適宜 `/Users/tyoyo/repos/tyoyo-cc-plugins/kirox/skills/kirox/references/refactor-impl-rules.md` にルールを追記するか提案すること
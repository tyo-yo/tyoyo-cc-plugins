# tyoyo-cc-plugins

個人用 Claude Code プラグインコレクション。

## プラグイン作成ルール

### ディレクトリ構造

```
plugin-name/
  .claude-plugin/
    plugin.json          # 必須: プラグインマニフェスト
  skills/                # オプション: スキル
    skill-name/
      SKILL.md           # メインスキルファイル
      SETUP.md           # セットアップガイド（必要に応じて）
  hooks/                 # オプション: フック
    hooks.json
  commands/              # オプション: コマンド
    command-name.md
  agents/                # オプション: エージェント
    agent-name.md
  README.md              # 推奨: 概要説明
```

### plugin.json の必須フィールド

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "短い説明",
  "author": { "name": "tyo-yo" },
  "license": "MIT"
}
```

---

## 公開ルール

新しいプラグインを追加したら **必ず** `.claude-plugin/marketplace.json` に追加する:

```json
{
  "name": "plugin-name",
  "source": "./plugin-name",
  "description": "説明",
  "version": "1.0.0",
  "author": { "name": "tyo-yo" },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

---

## コンポーネント別ベストプラクティス

### Skills（スキル）

スキルは Claude に専門知識を提供する。

**SKILL.md の構造**:
```markdown
---
name: skill-name
description: トリガーフレーズを含む説明。"create X", "use Y" のような具体的なフレーズを入れる。
allowed-tools: Bash(command:*)  # オプション: 許可するツール
---

# タイトル

## セクション1
...
```

**ベストプラクティス**:
- `description` にトリガーフレーズを含める（いつ読み込まれるか決まる）
- 本文は命令形で書く（「〜する」「〜を確認」）
- 1,500〜2,000語以内に収める
- 詳細は `references/` や `examples/` に分離（Progressive Disclosure）

### Hooks（フック）

フックはイベント駆動の自動化を提供する。

**イベント一覧**:
- `PreToolUse` / `PostToolUse`: ツール実行前後
- `Stop` / `SubagentStop`: セッション終了時
- `Notification`: 通知時

**hooks.json の例**:
```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/on-stop.ts"
      }
    ]
  }
}
```

**ベストプラクティス**:
- `${CLAUDE_PLUGIN_ROOT}` を使ってパスを指定（ポータビリティ）
- 複雑なロジックは `type: "prompt"` でプロンプトベースに
- `matcher` でツール名をフィルタ（PreToolUse/PostToolUse）

### Commands（コマンド）

ユーザーが `/plugin:command` で呼び出す。

**command-name.md の例**:
```markdown
---
name: command-name
description: コマンドの説明
argument-hint: "[arg1] [arg2]"
allowed-tools: Bash, Read, Write
---

# 指示内容

ここに Claude への指示を書く（ユーザーへの説明ではない）。
```

**ベストプラクティス**:
- `allowed-tools` は必要最小限に
- 本文は Claude への指示として書く

### Agents（エージェント）

自律的なタスク実行を行うサブエージェント。

**agent-name.md の例**:
```markdown
---
name: agent-name
when-to-use: |
  <example>
  Context: ユーザーがXをした後
  user: "Yをレビューして"
  assistant: "agent-name エージェントを使ってレビューします"
  </example>
model: sonnet
tools: Bash, Read, Grep, Glob
---

# System Prompt

あなたは〜の専門家です。
```

**ベストプラクティス**:
- `when-to-use` に具体的な `<example>` を含める
- `model` は `sonnet`（バランス）か `haiku`（高速）
- `tools` は必要最小限に

---

## コミット規約

```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント更新
refactor: リファクタリング
```

# カスタマイズ可能なコードレビュープラグイン設計書

作成日: 2026-02-10
対象: tyoyo-cc-plugins/custom-code-review

## 目次

1. [プラグイン概要](#プラグイン概要)
2. [アーキテクチャ設計](#アーキテクチャ設計)
3. [ディレクトリ構造](#ディレクトリ構造)
4. [設定ファイル仕様](#設定ファイル仕様)
5. [エージェント自動生成の仕組み](#エージェント自動生成の仕組み)
6. [コマンド仕様](#コマンド仕様)
7. [並列実行とスコアリング](#並列実行とスコアリング)
8. [拡張性の実現](#拡張性の実現)
9. [実装計画](#実装計画)

---

## プラグイン概要

### プラグイン名
**custom-code-review**

### 目的
ユーザーが自由にレビュー観点を追加・削除・カスタマイズできるコードレビュープラグイン。各観点ごとに専門エージェントを動的に生成し、並列実行で効率的にレビューを実施。

### 主要機能

1. **観点のカスタマイズ**
   - YAML設定ファイルで観点を管理
   - プリセット観点（30種類）から選択
   - カスタム観点の追加

2. **動的エージェント生成**
   - 設定に基づいてエージェントを自動生成
   - 各観点に特化したシステムプロンプト

3. **並列実行**
   - 複数エージェントを同時実行
   - グループ化による効率的な実行

4. **信頼度スコアリング**
   - すべての問題に0-100点のスコア
   - デフォルト80点以上のみ報告

5. **包括的なレポート**
   - Markdown形式の詳細レポート
   - GitHub PR コメント対応
   - 観点別・重大度別の集約

### 既存プラグインとの差別化

| 項目 | PR Review Toolkit | Feature Dev | Code Review | **custom-code-review** |
|------|-------------------|-------------|-------------|----------------------|
| 観点の固定/可変 | 固定（6観点） | 固定（3観点） | 固定（4観点） | **可変（ユーザー定義）** |
| エージェント数 | 6 | 3 | 4 | **1〜30+（設定次第）** |
| カスタム観点追加 | ❌ | ❌ | ❌ | **✅** |
| プリセット観点 | ❌ | ❌ | ❌ | **✅（30種類）** |
| 観点の有効化/無効化 | ❌ | ❌ | ❌ | **✅** |
| プロジェクト固有設定 | 部分的 | 部分的 | 部分的 | **✅（.local.md）** |

---

## アーキテクチャ設計

### システム構成図

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                            │
│          /custom-code-review [options]                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Configuration Loader                        │
│  - Load .claude/custom-code-review.local.md              │
│  - Merge with default config                             │
│  - Parse YAML frontmatter                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Agent Definition Generator                     │
│  - Generate agent MD files dynamically                   │
│  - Apply perspective templates                           │
│  - Inject custom prompts                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Parallel Execution Orchestrator               │
│  - Group agents by tier                                  │
│  - Launch agents in parallel                             │
│  - Collect results                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Confidence Score Filter                       │
│  - Extract confidence scores                             │
│  - Filter by threshold (default: 80)                     │
│  - Deduplicate issues                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Report Aggregator                           │
│  - Group by severity (Critical/Important/Minor)          │
│  - Group by perspective                                  │
│  - Generate markdown report                              │
│  - Optionally post to GitHub PR                          │
└─────────────────────────────────────────────────────────┘
```

### データフロー

```
1. User Command
   ↓
2. Load Configuration (.local.md)
   ↓
3. Validate & Merge with Defaults
   ↓
4. Generate Agent Definitions
   ↓
5. Prepare Review Context (git diff, CLAUDE.md, etc.)
   ↓
6. Launch Agents in Parallel Groups
   ├─ Tier 1 (Core) → Results 1
   ├─ Tier 2 (Recommended) → Results 2
   └─ Tier 3 (Optional) → Results 3
   ↓
7. Aggregate Results
   ↓
8. Filter by Confidence Score
   ↓
9. Deduplicate & Categorize
   ↓
10. Generate Report
   ↓
11. Output to Terminal / GitHub PR
```

---

## ディレクトリ構造

```
custom-code-review/
├── .claude-plugin/
│   ├── plugin.json                      # プラグインマニフェスト
│   └── marketplace.json                 # マーケットプレイス情報
│
├── commands/
│   └── review.md                        # メインコマンド
│
├── agents/
│   ├── _templates/                      # エージェントテンプレート
│   │   ├── tier1/                       # Tier 1エージェント（必須）
│   │   │   ├── guideline-enforcer.md
│   │   │   ├── bug-hunter.md
│   │   │   ├── security-guardian.md
│   │   │   ├── silent-failure-detector.md
│   │   │   └── test-quality-checker.md
│   │   ├── tier2/                       # Tier 2エージェント（推奨）
│   │   │   ├── edge-case-validator.md
│   │   │   ├── readability-enhancer.md
│   │   │   ├── architecture-analyst.md
│   │   │   ├── type-design-reviewer.md
│   │   │   └── comment-accuracy-checker.md
│   │   ├── tier3/                       # Tier 3エージェント（オプション）
│   │   │   ├── clean-code-mentor.md
│   │   │   ├── performance-auditor.md
│   │   │   ├── accessibility-checker.md
│   │   │   ├── git-history-analyzer.md
│   │   │   └── api-design-reviewer.md
│   │   └── custom-template.md           # カスタム観点のテンプレート
│   └── _generated/                      # 実行時に生成されるエージェント
│       └── .gitignore                   # 生成ファイルは無視
│
├── scripts/
│   ├── load-config.ts                   # 設定読み込み
│   ├── generate-agents.ts               # エージェント生成
│   ├── orchestrate-review.ts            # レビューオーケストレーション
│   ├── aggregate-results.ts             # 結果集約
│   └── post-to-github.ts                # GitHub PR投稿
│
├── config/
│   ├── default-perspectives.yaml        # デフォルト観点定義
│   ├── perspective-catalog.yaml         # 30観点カタログ
│   └── agent-prompts/                   # エージェントプロンプトライブラリ
│       ├── guideline-enforcer.txt
│       ├── bug-hunter.txt
│       ├── security-guardian.txt
│       └── ...
│
├── references/
│   ├── perspectives-guide.md            # 観点選択ガイド
│   ├── customization-guide.md           # カスタマイズガイド
│   └── best-practices.md                # ベストプラクティス
│
├── examples/
│   ├── minimal-config.yaml              # 最小構成例
│   ├── comprehensive-config.yaml        # 包括的構成例
│   ├── frontend-focused.yaml            # フロントエンド特化例
│   └── backend-security.yaml            # バックエンド・セキュリティ特化例
│
├── .local.md.template                   # 設定ファイルテンプレート
└── README.md                            # プラグイン説明
```

---

## 設定ファイル仕様

### ファイルパス
`.claude/custom-code-review.local.md`

### YAML Frontmatter

```yaml
---
# ============================================
# Custom Code Review Configuration
# ============================================

# レビュープロファイル（プリセット選択）
profile: comprehensive  # minimal, balanced, comprehensive, custom

# 有効化する観点（tier1, tier2, tier3, カスタム）
enabled_perspectives:
  # Tier 1: 必須（高優先度）
  - guideline-enforcer
  - bug-hunter
  - security-guardian
  - silent-failure-detector
  - test-quality-checker

  # Tier 2: 推奨（高〜中優先度）
  - edge-case-validator
  - readability-enhancer
  - architecture-analyst
  - type-design-reviewer
  - comment-accuracy-checker

  # Tier 3: オプション（中〜低優先度）
  # - clean-code-mentor
  # - performance-auditor
  # - accessibility-checker
  # - git-history-analyzer
  # - api-design-reviewer

# 無効化する観点（プロファイルから除外）
disabled_perspectives: []

# カスタム観点の定義
custom_perspectives:
  - name: domain-logic-validator
    description: "ドメインロジックの正確性と業務ルール準拠を検証"
    model: sonnet
    tier: 1
    focus_areas:
      - "業務ルールの正確な実装"
      - "ドメインモデルの不変条件"
      - "エンティティのライフサイクル管理"
      - "トランザクション境界の適切性"
    confidence_threshold: 85
    output_format: |
      **Domain Logic Issue**: [説明]
      - **Business Rule**: [該当する業務ルール]
      - **Location**: [ファイルパス:行番号]
      - **Impact**: [ビジネス影響]
      - **Fix**: [修正提案]
      - **Confidence**: [スコア]

# グローバル設定
global_settings:
  # 信頼度の閾値（この値以上のみ報告）
  confidence_threshold: 80

  # 並列実行の最大エージェント数
  max_parallel_agents: 4

  # レポート出力形式
  report_format: markdown  # markdown, json, html

  # GitHub PR コメント投稿
  post_to_github: false

  # レポート保存先
  report_output_path: /tmp/code-review-report.md

  # 詳細ログの出力
  verbose: false

# プロジェクト固有のルール強化
project_rules:
  # CLAUDE.md の場所（デフォルト: リポジトリルート）
  claude_md_paths:
    - ./CLAUDE.md
    - ./docs/CONTRIBUTING.md

  # 追加で参照するガイドラインファイル
  additional_guidelines:
    - ./docs/STYLE_GUIDE.md
    - ./docs/SECURITY.md

  # 無視するファイルパターン
  ignore_patterns:
    - "**/*.test.ts"
    - "**/*.spec.ts"
    - "**/generated/**"
    - "**/node_modules/**"

# 観点別のカスタマイズ
perspective_overrides:
  bug-hunter:
    confidence_threshold: 85  # より厳格に
    model: opus  # より強力なモデル

  accessibility-checker:
    enabled_only_for_paths:
      - "src/components/**"
      - "src/pages/**"

# 通知設定
notifications:
  # Critical問題が見つかった場合
  on_critical_issues:
    enabled: true
    method: terminal  # terminal, slack, email

  # レビュー完了時
  on_completion:
    enabled: false

---

# Custom Code Review Configuration

このファイルはカスタムコードレビュープラグインの設定です。

## 現在のプロファイル: comprehensive

有効な観点: 10個
- Tier 1: 5個（必須）
- Tier 2: 5個（推奨）
- Tier 3: 0個（無効）

カスタム観点: 1個
- domain-logic-validator

## 使用方法

```bash
# 設定を使用してレビュー実行
/custom-code-review:review

# 特定のtierのみ実行
/custom-code-review:review --tier 1

# カスタム観点のみ実行
/custom-code-review:review --custom-only

# GitHub PR にコメント投稿
/custom-code-review:review --post-to-github
```

## 設定の編集

このファイルの YAML frontmatter を編集して、観点を追加・削除・カスタマイズできます。

詳細は `${CLAUDE_PLUGIN_ROOT}/references/customization-guide.md` を参照してください。
```

### プロファイルのプリセット

#### minimal（最小構成）
```yaml
profile: minimal
# Tier 1の5つのみ有効
```

#### balanced（バランス型）
```yaml
profile: balanced
# Tier 1全て + Tier 2の一部（7-8個）
```

#### comprehensive（包括的）
```yaml profile: comprehensive
# Tier 1全て + Tier 2全て（10個）
```

#### custom（完全カスタム）
```yaml
profile: custom
# ユーザーが enabled_perspectives で完全制御
```

---

## エージェント自動生成の仕組み

### 生成プロセス

```typescript
// scripts/generate-agents.ts

interface PerspectiveConfig {
  name: string;
  description: string;
  model: 'opus' | 'sonnet' | 'haiku';
  tier: 1 | 2 | 3;
  focus_areas: string[];
  confidence_threshold: number;
  output_format?: string;
}

async function generateAgent(perspective: PerspectiveConfig): Promise<void> {
  // 1. テンプレート読み込み
  const templatePath = `${PLUGIN_ROOT}/agents/_templates/tier${perspective.tier}/${perspective.name}.md`;
  let template: string;

  if (existsSync(templatePath)) {
    // プリセット観点の場合：既存テンプレート使用
    template = await readFile(templatePath, 'utf-8');
  } else {
    // カスタム観点の場合：カスタムテンプレート使用
    template = await readFile(`${PLUGIN_ROOT}/agents/_templates/custom-template.md`, 'utf-8');

    // プロンプトライブラリから読み込み
    const promptPath = `${PLUGIN_ROOT}/config/agent-prompts/${perspective.name}.txt`;
    const customPrompt = existsSync(promptPath)
      ? await readFile(promptPath, 'utf-8')
      : generatePromptFromConfig(perspective);

    // テンプレート内の変数を置換
    template = template
      .replace('{{NAME}}', perspective.name)
      .replace('{{DESCRIPTION}}', perspective.description)
      .replace('{{MODEL}}', perspective.model)
      .replace('{{FOCUS_AREAS}}', perspective.focus_areas.join('\n- '))
      .replace('{{CONFIDENCE_THRESHOLD}}', perspective.confidence_threshold.toString())
      .replace('{{SYSTEM_PROMPT}}', customPrompt)
      .replace('{{OUTPUT_FORMAT}}', perspective.output_format || DEFAULT_OUTPUT_FORMAT);
  }

  // 2. 生成先ディレクトリ作成
  const outputDir = `${PLUGIN_ROOT}/agents/_generated`;
  await mkdir(outputDir, { recursive: true });

  // 3. エージェントファイル書き込み
  const outputPath = `${outputDir}/${perspective.name}.md`;
  await writeFile(outputPath, template, 'utf-8');

  console.log(`Generated agent: ${perspective.name} at ${outputPath}`);
}

function generatePromptFromConfig(perspective: PerspectiveConfig): string {
  return `
# ${perspective.name}

You are a specialized code review agent focusing on: ${perspective.description}

## Focus Areas

${perspective.focus_areas.map(area => `- ${area}`).join('\n')}

## Review Process

1. Analyze the code changes (git diff)
2. Identify issues related to your focus areas
3. Rate each issue with a confidence score (0-100)
4. Report only issues with confidence ≥ ${perspective.confidence_threshold}

## Output Format

${perspective.output_format || DEFAULT_OUTPUT_FORMAT}

## Important Guidelines

- Be thorough but not pedantic
- Focus on high-impact issues
- Provide actionable feedback
- Include file paths and line numbers
- Cite specific guidelines when applicable
- Avoid false positives
  `.trim();
}
```

### テンプレート例（プリセット観点）

```markdown
---
name: guideline-enforcer
when-to-use: |
  Use this agent proactively after code is written to ensure adherence to project guidelines.

  <example>
  Context: User has just completed a feature implementation
  user: "Review my code for guideline compliance"
  assistant: "I'll launch the guideline-enforcer agent to check compliance"
  </example>
model: sonnet
tools: Bash, Read, Grep, Glob
---

# Guideline Enforcer Agent

You are a specialized code review agent that enforces project-specific guidelines defined in CLAUDE.md and coding conventions.

## Mission

Ensure that code changes strictly adhere to:
1. CLAUDE.md explicit rules
2. Coding conventions and style guidelines
3. Existing codebase patterns

## Review Process

### Step 1: Load Guidelines

Read the following files:
- `CLAUDE.md` (repository root)
- Additional guideline files specified in configuration
- Related convention files in changed directories

### Step 2: Analyze Changes

For each changed file:
1. Identify the relevant guidelines
2. Check for violations
3. Cite specific rules from CLAUDE.md

### Step 3: Rate Confidence

Rate each issue on a 0-100 scale:
- 91-100: Explicit violation of a clearly stated rule in CLAUDE.md
- 80-90: Deviation from established conventions
- Below 80: Do not report

### Step 4: Report Issues

For each issue with confidence ≥ 80:

\`\`\`markdown
**Guideline Violation**: [description]
- **Guideline**: "CLAUDE.md says: [exact quote]"
- **Location**: [file:line]
- **Fix**: [suggestion]
- **Confidence**: [score]
\`\`\`

## Important Notes

- Always cite the exact guideline text
- Include file path and line number
- Provide concrete fix suggestions
- Do not report style issues covered by linters
- Focus on significant violations only

## Example Output

\`\`\`markdown
## Guideline Enforcement Results

### Critical Violations (91-100)

**Guideline Violation**: Using CommonJS require() instead of ES modules
- **Guideline**: "CLAUDE.md says: Always use ES module imports (import/export)"
- **Location**: src/utils/helper.ts:3
- **Fix**: Replace \`const fs = require('fs')\` with \`import fs from 'fs'\`
- **Confidence**: 95

### Important Issues (80-90)

**Guideline Violation**: Inconsistent naming - using snake_case for function
- **Guideline**: "CLAUDE.md says: Use camelCase for all functions and variables"
- **Location**: src/auth/validate_token.ts:12
- **Fix**: Rename \`validate_token\` to \`validateToken\`
- **Confidence**: 85
\`\`\`
```

### テンプレート例（カスタム観点）

```markdown
---
name: {{NAME}}
when-to-use: |
  {{DESCRIPTION}}
model: {{MODEL}}
tools: Bash, Read, Grep, Glob
---

# {{NAME}} Agent

{{SYSTEM_PROMPT}}

## Focus Areas

{{FOCUS_AREAS}}

## Confidence Threshold

Report only issues with confidence ≥ {{CONFIDENCE_THRESHOLD}}.

## Output Format

{{OUTPUT_FORMAT}}
```

---

## コマンド仕様

### メインコマンド: `/custom-code-review:review`

#### frontmatter

```yaml
---
name: review
description: |
  カスタマイズ可能なコードレビューを実行。設定ファイルに基づいて
  複数の専門エージェントを並列実行し、包括的なレビューレポートを生成。
argument-hint: "[--tier 1|2|3|all] [--custom-only] [--post-to-github] [--config PATH]"
allowed-tools: Bash, Read, Write, Task, Grep, Glob
---
```

#### コマンド本体

```markdown
# Custom Code Review Command

カスタマイズ可能なコードレビューを実行します。

## 実行フロー

### Phase 1: 設定読み込み

1. 設定ファイルのパスを決定
   - `--config` オプションで指定された場合：そのパスを使用
   - デフォルト：`.claude/custom-code-review.local.md`
   - 存在しない場合：テンプレートからコピー

2. 設定ファイルを読み込み
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/load-config.ts --config-path <path>
   ```

3. バリデーションとマージ
   - プロファイルの適用
   - enabled_perspectives の検証
   - custom_perspectives の検証
   - デフォルト値のマージ

### Phase 2: エージェント生成

1. 有効な観点のリストを取得

2. 各観点に対してエージェントファイルを生成
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/generate-agents.ts \
     --perspectives <JSON> \
     --output-dir ${CLAUDE_PLUGIN_ROOT}/agents/_generated
   ```

3. 生成されたエージェントの検証

### Phase 3: レビューコンテキスト準備

1. Git変更内容の取得
   ```bash
   git diff --cached  # Staged changes
   git diff           # Unstaged changes
   ```

2. CLAUDE.mdファイルの読み込み
   - リポジトリルートの CLAUDE.md
   - 追加のガイドラインファイル

3. PRメタデータの取得（該当する場合）
   ```bash
   gh pr view --json title,body,number
   ```

### Phase 4: エージェント実行

#### オプション処理

- `--tier 1`: Tier 1エージェントのみ実行
- `--tier 2`: Tier 1-2エージェントを実行
- `--tier 3` または `--tier all`: 全tierのエージェントを実行
- `--custom-only`: カスタム観点のみ実行
- デフォルト：Tier 1-2を実行

#### 並列実行

1. エージェントをグループ化
   ```typescript
   const groups = groupAgentsByTier(enabledAgents, options);
   // 例:
   // Group 1: Tier 1エージェント（4つ並列）
   // Group 2: Tier 2エージェント（4つ並列）
   // Group 3: Tier 3エージェント（4つ並列）
   ```

2. グループごとに並列実行
   ```bash
   # Group 1を並列実行（最大4エージェント）
   claude --agent ${CLAUDE_PLUGIN_ROOT}/agents/_generated/guideline-enforcer.md &
   claude --agent ${CLAUDE_PLUGIN_ROOT}/agents/_generated/bug-hunter.md &
   claude --agent ${CLAUDE_PLUGIN_ROOT}/agents/_generated/security-guardian.md &
   claude --agent ${CLAUDE_PLUGIN_ROOT}/agents/_generated/silent-failure-detector.md &
   wait

   # 結果を収集
   ```

3. 各エージェントの結果を収集
   - JSON形式で標準出力
   - ファイルに保存（/tmp/review-results/<agent-name>.json）

### Phase 5: 結果集約とフィルタリング

1. 全エージェントの結果を統合
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/aggregate-results.ts \
     --input-dir /tmp/review-results \
     --confidence-threshold <threshold>
   ```

2. 信頼度スコアでフィルタリング
   - デフォルト: 80以上のみ残す
   - 設定で閾値をカスタマイズ可能

3. 重複の除去
   - 同じファイル・行番号の問題をマージ
   - 最も信頼度の高いものを採用

4. カテゴリ別に分類
   - Critical (91-100)
   - Important (80-90)
   - 観点別グルーピング

### Phase 6: レポート生成

1. Markdownレポートの生成
   ```markdown
   # Code Review Report

   Date: 2026-02-10
   Configuration: comprehensive profile
   Agents Executed: 10
   Issues Found: 15 (Critical: 3, Important: 12)

   ## Summary

   | Perspective | Issues | Avg Confidence |
   |-------------|--------|----------------|
   | guideline-enforcer | 4 | 87 |
   | bug-hunter | 2 | 95 |
   | security-guardian | 1 | 100 |
   | ... | ... | ... |

   ## Critical Issues (91-100)

   ### 1. SQL Injection Vulnerability
   - **Perspective**: security-guardian
   - **Confidence**: 100
   - **Location**: src/api/users.ts:45-50
   - **Description**: [詳細]
   - **Fix**: [修正提案]

   ...
   ```

2. レポート出力
   - ターミナルに表示
   - ファイルに保存（設定で指定）
   - JSON形式でもエクスポート可能

### Phase 7: GitHub PR投稿（オプション）

`--post-to-github` フラグが指定された場合:

1. PRの存在確認
   ```bash
   gh pr view --json number
   ```

2. レビューコメントの投稿
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/post-to-github.ts \
     --report-path <path> \
     --pr-number <number>
   ```

3. インラインコメントの作成（オプション）
   - 各問題の Location に基づいてインラインコメント
   - GitHub の line comment API を使用

## エラーハンドリング

- 設定ファイルが不正な場合：エラーメッセージとテンプレートの場所を表示
- エージェント生成失敗：スキップして続行、警告を表示
- エージェント実行失敗：そのエージェントの結果を除外、警告を表示
- Git/GitHub操作失敗：該当機能を無効化、警告を表示

## 使用例

```bash
# デフォルト設定でレビュー実行
/custom-code-review:review

# Tier 1（必須）のみ実行
/custom-code-review:review --tier 1

# 全てのtierを実行
/custom-code-review:review --tier all

# カスタム観点のみ実行
/custom-code-review:review --custom-only

# GitHub PRにコメント投稿
/custom-code-review:review --post-to-github

# カスタム設定ファイルを使用
/custom-code-review:review --config ./my-review-config.md

# Tier 2まで実行し、PRにコメント
/custom-code-review:review --tier 2 --post-to-github
```

## 出力例

```
🔍 Custom Code Review Starting...

📋 Configuration loaded: comprehensive profile
✅ 10 perspectives enabled (Tier 1: 5, Tier 2: 5)
⚙️  Generating agents...
✅ 10 agents generated

🚀 Launching agents in parallel...

Group 1 (Tier 1): 5 agents
  ⏳ guideline-enforcer (sonnet)
  ⏳ bug-hunter (opus)
  ⏳ security-guardian (opus)
  ⏳ silent-failure-detector (sonnet)
  ⏳ test-quality-checker (sonnet)
✅ Group 1 complete (2m 15s)

Group 2 (Tier 2): 5 agents
  ⏳ edge-case-validator (sonnet)
  ⏳ readability-enhancer (haiku)
  ⏳ architecture-analyst (sonnet)
  ⏳ type-design-reviewer (sonnet)
  ⏳ comment-accuracy-checker (haiku)
✅ Group 2 complete (1m 45s)

📊 Aggregating results...
🔍 Found 27 issues
🎯 Filtered to 15 issues (confidence ≥ 80)

📝 Generating report...
✅ Report saved to /tmp/code-review-report.md

═══════════════════════════════════════════════════════
📊 REVIEW SUMMARY
═══════════════════════════════════════════════════════

Total Issues: 15
- Critical (91-100): 3
- Important (80-90): 12

Top Perspectives:
1. guideline-enforcer: 4 issues (avg confidence: 87)
2. bug-hunter: 2 issues (avg confidence: 95)
3. security-guardian: 1 issue (avg confidence: 100)

Full report: /tmp/code-review-report.md

═══════════════════════════════════════════════════════
```
```

---

## 並列実行とスコアリング

### 並列実行戦略

#### グループ化のロジック

```typescript
interface Agent {
  name: string;
  tier: 1 | 2 | 3;
  model: 'opus' | 'sonnet' | 'haiku';
  estimatedDuration: number; // seconds
}

function groupAgentsByTier(
  agents: Agent[],
  maxParallel: number = 4
): Agent[][] {
  const groups: Agent[][] = [];

  // Tier別にソート
  const sorted = agents.sort((a, b) => a.tier - b.tier);

  // Tierごとにグループ化
  for (const tier of [1, 2, 3]) {
    const tierAgents = sorted.filter(a => a.tier === tier);

    // maxParallel単位でグループ分割
    for (let i = 0; i < tierAgents.length; i += maxParallel) {
      groups.push(tierAgents.slice(i, i + maxParallel));
    }
  }

  return groups;
}
```

#### 実行タイミング

```
Timeline:
0:00 - Start
0:00 - Group 1 Launch (Tier 1, 4 agents in parallel)
  ├─ guideline-enforcer (sonnet, ~2min)
  ├─ bug-hunter (opus, ~2.5min)
  ├─ security-guardian (opus, ~2min)
  └─ silent-failure-detector (sonnet, ~1.5min)
2:30 - Group 1 Complete (最も遅いエージェントに依存)

2:30 - Group 2 Launch (Tier 1 remaining + Tier 2, 4 agents)
  ├─ test-quality-checker (sonnet, ~2min)
  ├─ edge-case-validator (sonnet, ~1.5min)
  ├─ readability-enhancer (haiku, ~1min)
  └─ architecture-analyst (sonnet, ~2min)
4:30 - Group 2 Complete

4:30 - Group 3 Launch (Tier 2 remaining, 4 agents)
  ├─ type-design-reviewer (sonnet, ~1.5min)
  ├─ comment-accuracy-checker (haiku, ~1min)
  └─ [other tier 2 agents]
6:00 - Group 3 Complete

6:00 - Aggregation & Reporting (~30sec)
6:30 - Complete

Total: ~6.5 minutes (15 agents)
Sequential would take: ~25 minutes
Speedup: 3.8x
```

### 信頼度スコアリング

#### スコアの定義

```markdown
| Score | Meaning | Action |
|-------|---------|--------|
| 91-100 | Certainty | Must fix - Critical bug or explicit violation |
| 80-90 | High confidence | Should fix - Important issue |
| 51-79 | Medium confidence | Consider fixing - Minor issue |
| 26-50 | Low confidence | Optional - Suggestion |
| 0-25 | Very low | Ignore - Likely false positive |

Default threshold: 80 (report 80-100 only)
```

#### スコア付与のガイドライン（エージェントへの指示）

```markdown
## Confidence Scoring Guidelines

Rate each issue based on:

### Certainty (100)
- Definite runtime error
- Explicit guideline violation (quoted from CLAUDE.md)
- Security vulnerability with clear exploit path
- Data loss scenario

### High (90)
- Very likely bug under specific conditions
- Strong guideline deviation
- High-impact security risk
- Missing critical test coverage

### Important (80-85)
- Probable logic error
- Inconsistent with established patterns
- Moderate security concern
- Inadequate error handling

### Medium (60-79)
- Possible issue
- Style inconsistency
- Minor quality concern
- Optimization opportunity

### Low (40-59)
- Questionable practice
- Subjective improvement
- Pedantic suggestion

### Very Low (0-39)
- Nitpick
- Personal preference
- Already handled elsewhere
- Not actually an issue

**Important**: Only report issues with confidence ≥ [THRESHOLD].
```

#### 重複除去のロジック

```typescript
interface Issue {
  perspective: string;
  confidence: number;
  location: string; // "file:line"
  description: string;
  fix: string;
}

function deduplicateIssues(issues: Issue[]): Issue[] {
  const grouped = new Map<string, Issue[]>();

  // Locationでグループ化
  for (const issue of issues) {
    const key = issue.location;
    if (!grouped.has(key)) {
      grouped.set(key, []);
    }
    grouped.get(key)!.push(issue);
  }

  // 各グループで最も信頼度の高いものを選択
  const deduplicated: Issue[] = [];
  for (const [location, group] of grouped) {
    // 信頼度でソート
    group.sort((a, b) => b.confidence - a.confidence);

    // 最も信頼度の高いものを採用
    const primary = group[0];

    // 他の観点も追記
    if (group.length > 1) {
      const others = group.slice(1).map(i => i.perspective).join(', ');
      primary.description += `\n\n**Also flagged by**: ${others}`;
    }

    deduplicated.push(primary);
  }

  return deduplicated;
}
```

---

## 拡張性の実現

### 1. 新しい観点の追加

#### ステップ1: カスタム観点の定義

`.claude/custom-code-review.local.md` に追加:

```yaml
custom_perspectives:
  - name: my-custom-check
    description: "My custom review perspective"
    model: sonnet
    tier: 2
    focus_areas:
      - "Check A"
      - "Check B"
    confidence_threshold: 80
```

#### ステップ2: プロンプトの作成（オプション）

`config/agent-prompts/my-custom-check.txt` を作成:

```markdown
# My Custom Check Agent

You are a specialized agent that checks for [specific concern].

## Review Process

1. [Step 1]
2. [Step 2]
...

## Output Format

**Issue**: [description]
- **Location**: [file:line]
- **Fix**: [suggestion]
- **Confidence**: [score]
```

#### ステップ3: レビュー実行

```bash
/custom-code-review:review
```

自動的に `my-custom-check` エージェントが生成・実行される。

### 2. プリセット観点の無効化

```yaml
disabled_perspectives:
  - accessibility-checker  # UI開発以外では不要
  - performance-auditor    # クリティカルパスでなければスキップ
```

### 3. 観点別の設定オーバーライド

```yaml
perspective_overrides:
  bug-hunter:
    confidence_threshold: 90  # より厳格に
    model: opus  # より強力なモデル

  test-quality-checker:
    focus_areas:
      - "振る舞いカバレッジ"
      - "エッジケーステスト"
      - "統合テスト品質"
```

### 4. プロジェクト固有のルール強化

```yaml
project_rules:
  additional_guidelines:
    - ./docs/DOMAIN_RULES.md
    - ./docs/API_CONVENTIONS.md

  ignore_patterns:
    - "**/legacy/**"  # レガシーコードは除外
```

### 5. パス別の観点有効化

```yaml
perspective_overrides:
  accessibility-checker:
    enabled_only_for_paths:
      - "src/components/**"
      - "src/pages/**"

  performance-auditor:
    enabled_only_for_paths:
      - "src/api/**"
      - "src/services/**"
```

### 6. 新しいプロファイルの作成

```yaml
# 例: frontend-focused プロファイル
profile: custom
enabled_perspectives:
  - guideline-enforcer
  - bug-hunter
  - security-guardian
  - accessibility-checker
  - type-design-reviewer
  - comment-accuracy-checker
  - readability-enhancer
```

保存して再利用:

```bash
# プロファイルをテンプレートとして保存
cp .claude/custom-code-review.local.md \
   custom-code-review/examples/frontend-focused.yaml

# 他のプロジェクトで使用
/custom-code-review:review --config ./path/to/frontend-focused.yaml
```

---

## 実装計画

### Phase 1: 基盤実装（Week 1）

- [x] プラグインディレクトリ構造作成
- [ ] plugin.json 作成
- [ ] 設定ファイルテンプレート作成
- [ ] デフォルト観点カタログ作成
- [ ] スクリプト基盤（TypeScript）
  - [ ] load-config.ts
  - [ ] generate-agents.ts

### Phase 2: コアエージェント実装（Week 1-2）

- [ ] Tier 1エージェントテンプレート作成
  - [ ] guideline-enforcer.md
  - [ ] bug-hunter.md
  - [ ] security-guardian.md
  - [ ] silent-failure-detector.md
  - [ ] test-quality-checker.md
- [ ] エージェント生成ロジック実装
- [ ] カスタムテンプレート実装

### Phase 3: オーケストレーション実装（Week 2）

- [ ] orchestrate-review.ts 実装
  - [ ] 並列実行ロジック
  - [ ] グループ化アルゴリズム
  - [ ] 結果収集
- [ ] aggregate-results.ts 実装
  - [ ] スコアフィルタリング
  - [ ] 重複除去
  - [ ] カテゴリ分類

### Phase 4: コマンドとレポート実装（Week 2-3）

- [ ] commands/review.md 実装
- [ ] レポート生成機能
  - [ ] Markdown形式
  - [ ] JSON形式
  - [ ] ターミナル出力
- [ ] post-to-github.ts 実装

### Phase 5: 追加エージェント実装（Week 3）

- [ ] Tier 2エージェントテンプレート作成
  - [ ] edge-case-validator.md
  - [ ] readability-enhancer.md
  - [ ] architecture-analyst.md
  - [ ] type-design-reviewer.md
  - [ ] comment-accuracy-checker.md
- [ ] Tier 3エージェントテンプレート作成
  - [ ] clean-code-mentor.md
  - [ ] performance-auditor.md
  - [ ] accessibility-checker.md
  - [ ] git-history-analyzer.md
  - [ ] api-design-reviewer.md

### Phase 6: ドキュメントと例（Week 3-4）

- [ ] README.md 作成
- [ ] references/
  - [ ] perspectives-guide.md
  - [ ] customization-guide.md
  - [ ] best-practices.md
- [ ] examples/
  - [ ] minimal-config.yaml
  - [ ] comprehensive-config.yaml
  - [ ] frontend-focused.yaml
  - [ ] backend-security.yaml

### Phase 7: テストとリファイン（Week 4）

- [ ] 実際のプロジェクトでテスト
- [ ] パフォーマンスチューニング
- [ ] エラーハンドリング強化
- [ ] ドキュメント改善

### Phase 8: マーケットプレイス登録（Week 4）

- [ ] marketplace.json 作成
- [ ] スクリーンショット作成
- [ ] 使用例動画作成（オプション）
- [ ] リリースノート作成

---

## まとめ

### 主要な設計上の決定

1. **動的エージェント生成**: 設定に基づいてエージェントを実行時に生成
2. **テンプレートベース**: プリセットとカスタムの両方をサポート
3. **並列実行**: 複数エージェントを効率的に並列実行
4. **信頼度スコアリング**: 偽陽性を削減
5. **YAML設定**: 柔軟で読みやすい設定形式
6. **.local.mdパターン**: プロジェクト固有設定とバージョン管理の分離

### 既存プラグインとの統合

- **PR Review Toolkit**: 観点定義の参考
- **Feature Dev**: ワークフロー統合の可能性
- **Code Review**: 並列実行パターンの参考

### 次のステップ

1. タスク#5（実装）に進む
2. Phase 1-2を優先実装
3. 実際のプロジェクトで早期テスト
4. フィードバックに基づいて改善

---

**設計書作成日**: 2026-02-10
**設計者**: Claude Sonnet 4.5
**バージョン**: 1.0.0

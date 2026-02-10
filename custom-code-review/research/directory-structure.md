# ディレクトリ構造設計：39観点マークダウンファイル

作成日: 2026-02-10
目的: Claude Codeプラグインのベストプラクティスに従い、39観点のマークダウンファイル構造を設計

---

## 📁 ディレクトリ構造

```
custom-code-review/
├── .claude-plugin/
│   └── plugin.json
├── references/
│   └── perspectives/
│       ├── INDEX.md                           # 目次ファイル（重要）
│       ├── project-standards/                 # カテゴリ1: プロジェクト標準（2観点）
│       │   ├── P01-ai-agent-instructions.md
│       │   └── P02-pattern-alignment.md
│       ├── correctness/                       # カテゴリ2: 正確性（5観点）
│       │   ├── C01-bug-detection.md
│       │   ├── C02-functional-compliance.md
│       │   ├── C03-edge-cases.md
│       │   ├── C04-silent-failures.md
│       │   └── C05-exception-safety.md
│       ├── security-basic/                    # カテゴリ3: セキュリティ基本（4観点）
│       │   ├── S01-basic-vulnerabilities.md
│       │   ├── S02-common-patterns.md
│       │   ├── S03-false-positive-filter.md
│       │   └── S04-precedent-based.md
│       ├── security-advanced/                 # カテゴリ4: セキュリティ高度（6観点）
│       │   ├── S05-adaptive-depth.md
│       │   ├── S06-attacker-modeling.md
│       │   ├── S07-security-regression.md
│       │   ├── S08-blast-radius.md
│       │   ├── S09-baseline-context.md
│       │   └── S10-red-flag-escalation.md
│       ├── testing/                           # カテゴリ5: テストとエラー処理（5観点）
│       │   ├── T01-test-coverage.md
│       │   ├── T02-test-quality.md
│       │   ├── T03-error-handling-quality.md
│       │   ├── T04-regression-tests.md
│       │   └── T05-e2e-test-plan.md
│       ├── quality/                           # カテゴリ6: 品質と保守性（4観点）
│       │   ├── Q01-readability.md
│       │   ├── Q02-complexity.md
│       │   ├── Q03-code-smells.md
│       │   ├── Q04-antipatterns.md
│       │   └── Q05-yagni-check.md
│       ├── design/                            # カテゴリ7: 設計とアーキテクチャ（6観点）
│       │   ├── D01-type-design.md
│       │   ├── D02-architecture-patterns.md
│       │   ├── D03-api-design.md
│       │   ├── D04-dependency-management.md
│       │   ├── D05-data-flow.md
│       │   └── D06-fix-review.md
│       ├── documentation/                     # カテゴリ8: ドキュメント（2観点）
│       │   ├── DOC01-comment-quality.md
│       │   └── DOC02-documentation-consistency.md
│       ├── performance/                       # カテゴリ9: パフォーマンス（3観点）
│       │   ├── PERF01-performance.md
│       │   ├── PERF02-accessibility.md
│       │   └── PERF03-resource-management.md
│       └── context/                           # カテゴリ10: コンテキスト分析（2観点）
│           ├── CTX01-git-history.md
│           └── CTX02-codebase-understanding.md
```

**合計**: 39ファイル + 1目次ファイル = 40ファイル

---

## 🗂️ ファイル命名規則

### 規則
- **フォーマット**: `{ID}-{kebab-case-name}.md`
- **ID**: カテゴリプレフィックス + 番号（例: P01, C01, S05）
- **名前**: ハイフン区切り、小文字のみ（例: ai-agent-instructions）

### カテゴリプレフィックス

| プレフィックス | カテゴリ | ファイル数 |
|--------------|---------|-----------|
| `P` | Project Standards（プロジェクト標準） | 2 |
| `C` | Correctness（正確性） | 5 |
| `S` | Security（セキュリティ） | 10 |
| `T` | Testing（テスト） | 5 |
| `Q` | Quality（品質） | 4 |
| `D` | Design（設計） | 6 |
| `DOC` | Documentation（ドキュメント） | 2 |
| `PERF` | Performance（パフォーマンス） | 3 |
| `CTX` | Context（コンテキスト） | 2 |

### ファイル命名例

- ✅ `P01-ai-agent-instructions.md`
- ✅ `S07-security-regression.md`
- ✅ `DOC01-comment-quality.md`
- ❌ `P01_ai_agent_instructions.md`（アンダースコア不可）
- ❌ `p01-ai-agent-instructions.md`（大文字必須）
- ❌ `ai-agent-instructions.md`（ID必須）

---

## 📄 マークダウンファイルのフォーマット

### テンプレート構造

```markdown
# {観点名（日本語）}

**ID**: {ID}
**カテゴリ**: {カテゴリ名}
**優先度**: {Tier 1/2/3}
**信頼度基準**: {基準}

---

## 参照元

- [{ソース名}]({GitHub URL})
- [{記事タイトル}]({記事URL})

---

## 概要

{観点の目的と重要性を1-2段落で説明}

---

## チェック内容

- {チェック項目1}
- {チェック項目2}
- {チェック項目3}
  - {サブ項目}
  - {サブ項目}

---

## 適用基準

### 使用する場合

- ✅ {条件1}
- ✅ {条件2}

### 使用しない場合

- ❌ {条件1}
- ❌ {条件2}

---

## 具体例

### ❌ 悪い例

\`\`\`{language}
{コード例}
\`\`\`

**問題点**: {説明}

### ✅ 良い例

\`\`\`{language}
{コード例}
\`\`\`

**理由**: {説明}

---

## 2026年トレンド

{該当する場合のみ記載}

---

## 関連観点

- [{関連観点ID}] {関連観点名}
- [{関連観点ID}] {関連観点名}
```

### フォーマットのポイント

1. **H2セクション（##）を使用**: フラットな構造
2. **箇条書き中心**: 一つ一つの項目が独立して削除・追加可能
3. **日本語記述**: すべて日本語で記載
4. **URLは必須**: 参照元セクションに必ず記載
5. **具体例を含む**: コード例で理解を促進

---

## 📋 INDEX.md（目次ファイル）の設計

### 目的
- 「どの観点をいつ読むべきか」を明確にする
- 無駄な読み込みを防ぐ
- 効率的なナビゲーション

### 構成

1. **カテゴリ別観点リスト**
   - 10カテゴリ × 各観点のリンク
   - ファイルパス、優先度、説明を含む

2. **PRタイプ別推奨観点**
   - 新機能追加 → どの観点を読むべきか
   - バグ修正 → どの観点を読むべきか
   - リファクタリング → どの観点を読むべきか
   - セキュリティ修正 → どの観点を読むべきか
   - etc.

3. **ファイルタイプ別推奨観点**
   - 認証・認可 → S01, S02, S06, S07推奨
   - API エンドポイント → C01, S01, C03推奨
   - データベース → C01, S01, PERF03推奨
   - UI コンポーネント → Q01, D02推奨
   - etc.

4. **Tier別観点リスト**
   - Tier 1（必須）: 常に適用
   - Tier 2（推奨）: 高価値
   - Tier 3（オプション）: 特定シナリオ

5. **検索ガイド**
   - キーワードで探す場合
   - 問題から探す場合
   - 言語別の推奨観点

---

## 🔧 実装計画

### フェーズ1: ディレクトリ作成
```bash
mkdir -p custom-code-review/references/perspectives/{project-standards,correctness,security-basic,security-advanced,testing,quality,design,documentation,performance,context}
```

### フェーズ2: バッチ分割（10バッチ × 各4観点前後）

| バッチ | 観点範囲 | カテゴリ | ファイル数 |
|--------|---------|---------|-----------|
| 1 | P01-P02 | プロジェクト標準 | 2 |
| 2 | C01-C05 | 正確性 | 5 |
| 3 | S01-S04 | セキュリティ基本 | 4 |
| 4 | S05-S10 | セキュリティ高度 | 6 |
| 5 | T01-T05 | テスト | 5 |
| 6 | Q01-Q05 | 品質 | 4 |
| 7 | D01-D06 | 設計 | 6 |
| 8 | DOC01-DOC02 | ドキュメント | 2 |
| 9 | PERF01-PERF03 | パフォーマンス | 3 |
| 10 | CTX01-CTX02 | コンテキスト | 2 |

**合計**: 39ファイル

### フェーズ3: サブエージェント並列実行
- バッチ1-5を5つのサブエージェントで並列実行（第1波）
- バッチ6-10を5つのサブエージェントで並列実行（第2波）

---

## 📚 ベストプラクティス

### DO（推奨）

✅ **IDベース命名**: ファイル名にIDを含める
✅ **カテゴリ分類**: 関連観点をサブディレクトリにまとめる
✅ **フラット構造**: H2セクション中心、深いネストを避ける
✅ **箇条書き**: 削除・追加が容易な形式
✅ **具体例**: コード例で理解を促進
✅ **URLリンク**: 参照元を必ず記載

### DON'T（非推奨）

❌ **深いネスト**: H3、H4を多用しない
❌ **長文**: 1セクション1段落を目安
❌ **重複**: 複数ファイルで同じ内容を書かない
❌ **抽象的**: 具体例なしの説明
❌ **英語**: すべて日本語で記載

---

## 🎯 次のステップ

1. ✅ ディレクトリ構造設計（このファイル）
2. ⏭️ INDEX.md作成（Task #8）
3. ⏭️ バッチ1-10のマークダウンファイル作成（Task #9-13）

---

**作成日**: 2026-02-10
**設計者**: Claude Sonnet 4.5
**ファイル数**: 40（39観点 + 1目次）

# Haystack Documentation Command Example

This is a real-world example of a documentation command created using the knowledge-pathfinder workflow. It demonstrates the complete structure and best practices for a large, comprehensive library.

## Key Features Demonstrated

- ✅ **Comprehensive URL collection**: 150+ URLs across all major sections
- ✅ **Clear categorization**: 15 major sections with subsections
- ✅ **Importance markers**: 🔥 marks on essential pages
- ✅ **Three-level access strategy**: WebFetch → DeepWiki → Repomix
- ✅ **Concrete examples**: 5 WebFetch examples for common use cases
- ✅ **Repository verification**: Correct repo name with confusion warnings
- ✅ **Japanese language**: Entire file in Japanese for consistency

## File Structure Excerpt

```markdown
# Haystack ドキュメント参照コマンド

## 概要

Haystackは、本番環境対応のAIエージェント、強力なRAGアプリケーション、スケーラブルな
マルチモーダル検索システムを構築するためのオープンソースAIフレームワークです。

## 重要な注意点

- **パッケージ名**: `haystack-ai`（`farm-haystack`と混同しないこと）
- **同じPython環境に両方インストールしない**: 問題が発生します
- **バージョン管理**: ドキュメントは複数バージョン（2.18-2.24-unstable）が利用可能

## ドキュメント構造

### 1. Getting Started
- **Introduction** 🔥: https://docs.haystack.deepset.ai/docs/intro - 基本概念と特徴
- **Get Started** 🔥: https://docs.haystack.deepset.ai/docs/get-started - RAGパイプライン構築
- **Installation**: https://docs.haystack.deepset.ai/docs/installation - インストール手順

### 2. Core Concepts
- **Haystack Concepts Overview** 🔥: https://... - 全体像
- **Components** 🔥: https://... - コンポーネントシステム
- **Pipelines** 🔥: https://... - パイプラインの基本

[... 46 Generators, 30+ Retrievers, 40 Embedders, 23 Converters ...]

## ドキュメントへのアクセス方法

### 方法1: WebFetch（公式ドキュメント）- 最優先

#### 使用例

```typescript
// 例1: RAGパイプライン構築の基本を学ぶ
WebFetch({
  url: "https://docs.haystack.deepset.ai/docs/get-started",
  prompt: "RAGパイプラインの構築手順とコード例を詳しく教えてください"
})

// 例2: 特定のGeneratorの使用方法を確認
WebFetch({
  url: "https://docs.haystack.deepset.ai/docs/openaichatgenerator",
  prompt: "OpenAIChatGeneratorの初期化方法、パラメータ、使用例を教えてください"
})

// 例3: エージェントシステムの理解
WebFetch({
  url: "https://docs.haystack.deepset.ai/docs/agents",
  prompt: "Haystackのエージェントシステムのアーキテクチャと実装方法を説明してください"
})
```

### 方法2: DeepWiki MCP（アーキテクチャと実装詳細）

**重要**: `deepset-ai/haystack` を指定してください

```typescript
// リポジトリ構造の確認
mcp__deepwiki__read_wiki_structure({
  repoName: "deepset-ai/haystack"
})

// 特定のトピックについて質問（日本語で質問すること）
mcp__deepwiki__ask_question({
  repoName: "deepset-ai/haystack",
  question: "パイプラインシステムのアーキテクチャと実装の詳細を教えてください"
})
```

## 推奨アプローチ

### レベル1: WebFetch（最優先）
- 基本的な使い方の確認
- コンポーネント/API仕様
- 実装例とベストプラクティス

### レベル2: DeepWiki MCP（中程度の詳細度）
- アーキテクチャ理解
- 内部実装の詳細
- コンポーネント間の連携

### レベル3: Repomix MCP（最も詳細、最終手段）
- ソースコード確認
- バグ調査
```

## Creation Process Used

This command was created following the exact workflow in SKILL.md:

### Phase 1: URL Collection
- **WebFetch**: Used to extract navigation structure from main docs page
- **WebSearch**: Ran 5 parallel searches with `site:docs.haystack.deepset.ai`
  - General: "Haystack documentation site:docs.haystack.deepset.ai 2026"
  - Components: "Haystack generators retrievers site:docs.haystack.deepset.ai"
  - Embedders: "Haystack embedders converters rankers site:docs.haystack.deepset.ai"
  - Document Stores: "Haystack document stores InMemory Chroma site:docs.haystack.deepset.ai"
  - Tutorials: "Haystack tutorials cookbooks examples site:docs.haystack.deepset.ai"
- **Section deep-dive**: Used WebFetch on 8 major sections to get detailed lists
  - Concepts, Pipelines, Generators, Retrievers, Embedders, Converters, Evaluation, etc.

**Result**: Collected 150+ URLs covering all major sections

### Phase 2: Content Sampling
- Sampled 10 major pages with WebFetch
- Categorized each by type (tutorial, API reference, guide)
- Marked essential pages with 🔥 (Getting Started, Core Concepts, major component lists)

### Phase 3: Repository Verification
```typescript
mcp__deepwiki__read_wiki_structure({
  repoName: "deepset-ai/haystack"
})
```
- Confirmed correct repository name
- Documented available DeepWiki sections in command file
- No similar repo confusion (single main repo)

### Phase 4: Command File Creation
- Used template structure from `references/template.md`
- Wrote entire file in Japanese
- Included 5 concrete WebFetch examples covering:
  1. Building RAG pipelines
  2. Using specific Generators
  3. Understanding Agent system
  4. Choosing Document Stores
  5. Implementing evaluation

### Phase 5: Quality Assurance
- Verified all URLs accessible
- Tested DeepWiki access
- Confirmed WebFetch examples work
- All checklist items passed

## Statistics

- **Total URLs**: ~150
- **Major sections**: 15
- **🔥 marked pages**: 23
- **WebFetch examples**: 5
- **Word count**: ~2,800 (Japanese)
- **Creation time**: ~30 minutes using the workflow

## Lessons Learned

1. **WebFetch + WebSearch is sufficient**: No Playwright needed for comprehensive URL collection
2. **Parallel queries are essential**: Running 5+ WebSearch queries simultaneously saved significant time
3. **Deep-dive on major sections**: After initial discovery, drilling into specific sections (Generators, Retrievers, etc.) revealed 100+ additional URLs
4. **Repository verification is critical**: Testing DeepWiki access prevented documenting incorrect repo name
5. **Concrete examples matter**: Generic WebFetch examples are less useful than specific, copy-pastable ones

## File Location

See the complete file at: `.claude/commands/docs/haystack.md`

This example demonstrates that the knowledge-pathfinder workflow can handle large, complex documentation sites effectively without requiring Playwright or manual URL collection.

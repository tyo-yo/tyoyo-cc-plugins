---
name: knowledge-pathfinder
description: このスキルは、ユーザーが「ドキュメント参照コマンドを作成」「ライブラリのドキュメントを整理」「Webリソースを構造化」「LLM用にドキュメントをインデックス化」と依頼した場合、またはライブラリドキュメント、APIリファレンス、企業サイトなどのWebリソースへの構造化されたアクセスを作成することに言及した場合に使用する。
version: 0.2.0
---

# Documentation Command Creation Guide (2026 Edition)

Create optimized documentation reference commands using modern standards (llms.txt, sitemap.xml) and category-specific strategies for comprehensive, efficient URL collection without expensive crawling services.

## Purpose

This skill guides creation of structured documentation reference commands that:
- **Leverage modern standards**: Check llms.txt and sitemap.xml first (free, comprehensive)
- **Use category-specific strategies**: GitHub OSS, Enterprise sites, API docs each have optimal approaches
- **Define intelligent access patterns**: WebFetch → DeepWiki → Repomix with token efficiency
- **Achieve near-complete coverage**: 95-100% URL coverage without manual crawling or paid services

The result is a command file (like `.claude/commands/docs/haystack.md`) that serves as a knowledge pathfinder for the target resource.

## When to Use This Skill

Use this skill when creating documentation reference commands for:
- Open source library documentation (React, Haystack, Next.js, etc.)
- Enterprise websites and knowledge bases
- API documentation and references
- SaaS product documentation
- Any web resource requiring structured LLM access

## Modern Workflow (2026 Edition)

Follow these phases in order. Phase 0 is new and critical for efficiency.

### Phase 0: Resource Discovery & Type Detection

**Goal**: Identify the most efficient collection method before manual work.

**Note**: The TypeScript examples throughout this guide are illustrative representations of Claude Code tool calls. The actual tool invocation syntax may differ slightly, but the concepts and parameters shown are accurate.

#### Step 0.1: Check for llms.txt (Highest Priority)

llms.txt is a 2024 standard adopted by 844,000+ sites including Anthropic, Cloudflare, and Stripe. It provides a curated list of URLs optimized for LLMs.

```typescript
// Primary llms.txt
WebFetch({
  url: "https://docs.example.com/llms.txt",
  prompt: "このllms.txtファイルを解析し、提供されているすべてのドキュメントURL、セクション、説明を構造化して抽出してください"
})

// Full version (if available)
WebFetch({
  url: "https://docs.example.com/llms-full.txt",
  prompt: "完全版のドキュメントURLリストを抽出してください"
})
```

**If llms.txt exists**:
- ✅ 95-100% coverage achieved in 1 minute
- ✅ URLs already categorized
- ✅ Skip to Phase 2 (Content Sampling)

**llms.txt format**:
```markdown
# Project Name

> Brief description

## Section 1
- [Page Title](URL): Description
- [Page Title](URL): Description

## Optional
- [Advanced Topic](URL): Description
```

#### Step 0.2: Check for sitemap.xml (Second Priority)

If llms.txt doesn't exist, check sitemap.xml - a standard format with 50,000 URL capacity.

```typescript
// Check primary sitemap
WebFetch({
  url: "https://docs.example.com/sitemap.xml",
  prompt: "このsitemap.xmlからすべてのURLを抽出してください。<sitemap>タグがある場合（sitemap index）は、子sitemapのURLもリストアップしてください"
})

// Check robots.txt for sitemap location
WebFetch({
  url: "https://docs.example.com/robots.txt",
  prompt: "'Sitemap:'で始まる行を探し、sitemapの場所を教えてください"
})

// If sitemap index found, fetch child sitemaps
WebFetch({
  url: "https://docs.example.com/sitemap-docs.xml",
  prompt: "このsitemapから文書ページのURLをすべて抽出してください"
})
```

**If sitemap.xml exists**:
- ✅ 90-100% coverage in 2-3 minutes
- ✅ All URLs in one place
- ⚠️ May need categorization (proceed to Phase 2)

**Free sitemap extraction tools** (alternative if WebFetch struggles):
- SiteGPT Sitemap Extractor: https://sitegpt.ai/tools/sitemap-url-extractor
- Direct XML parsing

#### Step 0.3: Determine Resource Category

Identify the resource type to select optimal collection strategy:

```typescript
WebFetch({
  url: "https://docs.example.com/",
  prompt: "このサイトのタイプを判定してください：1) GitHubのOSSライブラリドキュメント、2) 企業/SaaSのドキュメントサイト、3) APIドキュメント、4) その他。また、GitHub リポジトリへのリンクがあるか、OpenAPI/Swagger仕様があるかも確認してください"
})
```

**Categories**:
- **A. GitHub OSS Library**: Has GitHub repo, open source project
- **B. Enterprise/SaaS Documentation**: Company product docs, hosted on custom domain
- **C. API Documentation**: REST/GraphQL API references, may have OpenAPI spec
- **D. Other**: Blogs, wikis, knowledge bases

#### Step 0.4: Select Optimal Strategy

Based on Steps 0.1-0.3, determine the collection approach:

| Condition | Strategy | Expected Coverage | Time |
|-----------|----------|-------------------|------|
| llms.txt exists | Use llms.txt → Phase 2 | 95-100% | 1 min |
| sitemap.xml exists | Use sitemap.xml → Phase 2 | 90-100% | 3 min |
| GitHub OSS + no llms.txt/sitemap | Strategy A (Phase 1A) | 85-95% | 10 min |
| Enterprise/SaaS + no standards | Strategy B (Phase 1B) | 70-90% | 15 min |
| API Docs + OpenAPI spec | Strategy C (Phase 1C) | 95-100% | 5 min |
| Other | Fallback (Phase 1D) | 70-85% | 15 min |

### Phase 1: Category-Specific URL Collection

**Only execute this phase if Phase 0 didn't find llms.txt or sitemap.xml.**

Choose the strategy matching your resource category from Step 0.3.

#### Strategy A: GitHub OSS Libraries

**Best for**: React, Vue, Next.js, Haystack, etc.

**Step A.1: Repository Information**

```typescript
// Identify GitHub repository
WebFetch({
  url: "https://docs.example.com/",
  prompt: "このドキュメントサイトに関連するGitHubリポジトリのURLを見つけてください（通常はヘッダーやフッターにあります）"
})
```

**Step A.2: DeepWiki Structure**

```typescript
mcp__deepwiki__read_wiki_structure({
  repoName: "org/repo-name"  // Verify exact name
})
```

**Step A.3: GitHub-Specific Resources**

```typescript
// Check for GitHub Pages
WebFetch({
  url: "https://org.github.io/repo-name/",
  prompt: "GitHub Pagesのドキュメント構造とURLを抽出してください"
})

// Check main branch docs
WebFetch({
  url: "https://github.com/org/repo-name/tree/main/docs",
  prompt: "docs/ディレクトリ内のMarkdownファイルとその構造をリストアップしてください"
})
```

**Step A.4: Official Documentation Site**

If the project has a separate docs site (docs.example.com), use Strategy B on that domain.

**Coverage**: 85-95% (GitHub + docs site + DeepWiki)

#### Strategy B: Enterprise/SaaS Documentation

**Best for**: Stripe, Twilio, company products without llms.txt/sitemap.

**Step B.1: Navigation Structure Extraction**

```typescript
WebFetch({
  url: "https://docs.example.com/",
  prompt: "ナビゲーション構造（サイドバー、トップメニュー、フッター）からすべてのドキュメントセクションとURLを抽出してください。Getting Started、API Reference、Guides、Tutorials などの主要カテゴリを特定してください"
})
```

**Step B.2: Comprehensive Search**

Run 5-8 parallel WebSearch queries with `site:` operator:

```typescript
// General search
WebSearch({ query: "site:docs.example.com [product-name] documentation 2026" })

// Category-specific searches
WebSearch({ query: "site:docs.example.com getting started tutorial" })
WebSearch({ query: "site:docs.example.com API reference" })
WebSearch({ query: "site:docs.example.com guides examples" })
WebSearch({ query: "site:docs.example.com configuration setup" })
WebSearch({ query: "site:docs.example.com troubleshooting FAQ" })
```

**Run searches in parallel** for efficiency.

**Step B.3: Section Deep-Dive**

For each major section discovered, fetch detailed URL lists:

```typescript
WebFetch({
  url: "https://docs.example.com/api-reference",
  prompt: "このAPIリファレンスページから、すべてのエンドポイント、メソッド、リソースのドキュメントURLをリストアップしてください"
})

WebFetch({
  url: "https://docs.example.com/guides",
  prompt: "すべてのガイド記事のURLとトピックを抽出してください"
})
```

**Coverage**: 70-90% (depends on site structure)

#### Strategy C: API Documentation

**Best for**: REST APIs, GraphQL APIs with OpenAPI/Swagger specs.

**Step C.1: Check for API Spec**

```typescript
// OpenAPI/Swagger spec
WebFetch({
  url: "https://api.example.com/openapi.json",  // or swagger.json, openapi.yaml
  prompt: "このOpenAPI仕様からすべてのエンドポイント、タグ、ドキュメントURLを抽出してください"
})

// Alternative locations
WebFetch({ url: "https://docs.example.com/api/openapi.json", prompt: "..." })
WebFetch({ url: "https://docs.example.com/swagger.json", prompt: "..." })
```

**Step C.2: GraphQL Schema (if applicable)**

```typescript
WebFetch({
  url: "https://api.example.com/graphql/schema",
  prompt: "GraphQLスキーマからすべてのクエリ、ミューテーション、タイプのドキュメントを抽出してください"
})
```

**Step C.3: Documentation Pages**

Use Strategy B for human-readable documentation pages.

**Coverage**: 95-100% (if OpenAPI spec exists)

#### Fallback: Traditional WebFetch + WebSearch

**Use when**: None of the above strategies apply or as supplementary method.

This is the original workflow from version 0.1.0:

1. WebFetch on main page for navigation
2. Multiple parallel WebSearch with `site:` operator
3. Deep-dive on major sections

**Coverage**: 70-85%

### Phase 2: Content Sampling

**Goal**: Understand page content and assign importance ratings.

Sample 5-10 major pages from each category:

```typescript
WebFetch({
  url: "https://docs.example.com/getting-started",
  prompt: "このページの主な内容を簡潔にまとめてください。対象読者（初心者/上級者）、内容タイプ（チュートリアル/リファレンス/ガイド）、重要度を判断してください"
})
```

For each sampled page, record:
- **Content type**: Tutorial, API reference, concept explanation, guide
- **Target audience**: Beginner, intermediate, advanced
- **Importance**: Essential (🔥), important, optional
- **Category**: Which section it belongs to

**Coverage checklist**:
- [ ] Getting Started / Installation
- [ ] Core Concepts / Architecture
- [ ] API / Component references
- [ ] Configuration / Setup
- [ ] Advanced topics
- [ ] Examples / Tutorials
- [ ] Troubleshooting / FAQ

### Phase 3: Repository Verification

**Goal**: Verify GitHub repository information for DeepWiki/Repomix access.

**Only needed for resources with GitHub repos** (usually GitHub OSS libraries).

#### Step 3.1: Confirm Repository Name

```typescript
mcp__deepwiki__read_wiki_structure({
  repoName: "org/repo-name"  // Test exact name
})
```

**Common pitfalls**:
- Server implementation vs client SDK (e.g., `grpc/grpc` vs `grpc/grpc-web`)
- Main project vs docs repo (e.g., `facebook/react` vs `facebook/react-docs`)
- Language-specific SDKs (e.g., `stripe/stripe-python` vs `stripe/stripe-node`)

**If uncertain, ask the user**: "このライブラリのGitHubリポジトリは `org/repo-a` と `org/repo-b` のどちらが正しいですか？"

#### Step 3.2: Document DeepWiki Availability

Record the table of contents from DeepWiki for the command file.

### Phase 4: Command File Creation

**Goal**: Generate structured command file using template.

#### Step 4.1: File Location and Language

Create at: `.claude/commands/docs/[library-name].md`

**Write entirely in Japanese** for consistency with existing doc commands.

#### Step 4.2: Structure and Content

Follow the template in `references/template.md`. Key sections:

1. **概要**: 1-2 sentence library description
2. **重要な注意点**: Package names, similar libraries, version notes
3. **ドキュメント構造**: Categorized URLs with 🔥 for essential pages
4. **アクセス方法**:
   - 方法1: WebFetch (最優先) - 3-5 concrete examples
   - 方法2: DeepWiki MCP - Repository name with warnings
   - 方法3: Repomix MCP - Token efficiency warnings
5. **推奨アプローチ**: Three-level strategy explanation
6. **クイックリファレンス**: Common use case shortcuts
7. **トラブルシューティング**: 2-4 common issues

#### Step 4.3: Document Collection Method Used

Add a note about which collection method was used:

```markdown
## 作成方法

このコマンドは以下の方法で作成されました:
- ✅ llms.txt から URL を収集（95%カバレッジ）
- ✅ WebSearchで追加ページを発見（5%）
- ✅ DeepWiki で deepset-ai/haystack を確認
```

This helps future maintainers update the command efficiently.

#### Step 4.4: WebFetch Examples

Include 3-5 practical, copy-pastable examples:

```typescript
// 例1: 基本的な使い方を学ぶ
WebFetch({
  url: "https://docs.example.com/getting-started",
  prompt: "[ライブラリ名]の基本的な使い方とセットアップ手順を詳しく教えてください"
})

// 例2: 特定のコンポーネント/APIを調べる
WebFetch({
  url: "https://docs.example.com/api/component",
  prompt: "[Component名]の初期化方法、プロパティ、メソッド、使用例を教えてください"
})
```

### Phase 5: Quality Assurance

**Goal**: Ensure command file meets quality standards.

#### Step 5.1: Coverage Verification

Check coverage against collection method:

| Method | Expected Coverage | Verification |
|--------|-------------------|--------------|
| llms.txt | 95-100% | Compare with sitemap.xml if available |
| sitemap.xml | 90-100% | Spot-check major sections |
| Strategy A-C | 85-95% | Check for missing major sections |
| Fallback | 70-85% | Accept lower coverage, note gaps |

#### Step 5.2: Self-Check Checklist

```
[ ] 全体が日本語で記述されている
[ ] 収集方法を文書化している（llms.txt, sitemap.xml, etc.）
[ ] URLは正確（サンプルでアクセス確認済み）
[ ] リポジトリ名は正確（DeepWikiでアクセス確認済み）
[ ] 混同しやすいライブラリを明示（該当する場合）
[ ] 主要セクションをカバー（Getting Started, API, Guides等）
[ ] WebFetch例が具体的で実用的（3-5個）
[ ] DeepWiki使用例にリポジトリ名の注意書き
[ ] Repomix使用例にトークン消費の警告
[ ] 重要ページに🔥マーク
[ ] 初見の人が理解できる説明
[ ] コードブロックの構文が正しい
```

#### Step 5.3: Verification Testing

Test key components:

```typescript
// Test primary URL
WebFetch({
  url: "[重要なURL]",
  prompt: "このページの主な内容を確認"
})

// Test DeepWiki access (if applicable)
mcp__deepwiki__read_wiki_structure({
  repoName: "[指定したリポジトリ名]"
})
```

#### Step 5.4: User Review

If uncertain about:
- Correct repository name (especially with similar repos)
- Distinction from similar libraries
- Importance ratings (🔥 markers)
- Coverage completeness

**Ask the user for clarification** rather than making assumptions.

## Best Practices (2026 Edition)

### Collection Efficiency

1. **Always check modern standards first**:
   - llms.txt (1 minute, 95-100% coverage)
   - sitemap.xml (3 minutes, 90-100% coverage)
   - Then manual methods (15+ minutes, 70-90% coverage)

2. **Use category-specific strategies**:
   - GitHub OSS: DeepWiki + GitHub Pages + docs site
   - Enterprise/SaaS: WebFetch + WebSearch
   - API: OpenAPI spec + docs site

3. **Parallelize when possible**:
   - Run multiple WebSearch queries simultaneously
   - Fetch multiple sections concurrently
   - Process sitemap indexes in parallel

4. **Document your method**:
   - Note which collection method achieved what coverage
   - Helps future updates

### Repository Information

1. **Always verify with DeepWiki** before documenting repo name
2. **Highlight confusion risks** (similar repo names, SDK variants)
3. **Ask when uncertain** - better to confirm than document incorrectly

### Command File Quality

1. **Write in Japanese** - consistency with existing commands
2. **Include concrete examples** - copy-pastable WebFetch calls
3. **Prioritize progressive access** - WebFetch → DeepWiki → Repomix
4. **Mark essential pages** - use 🔥 sparingly (1-3 per section)
5. **Document collection method** - llms.txt, sitemap.xml, or manual

### Token Efficiency

1. **Favor llms.txt/sitemap.xml** - pre-curated, comprehensive
2. **WebFetch for quick lookups** - smallest token footprint
3. **DeepWiki for architecture** - when docs are insufficient
4. **Repomix as last resort** - highest token cost

## Modern Standards Reference

### llms.txt Format

```markdown
# Project Name

> One-line description

## Getting Started
- [Installation](URL): How to install
- [Quick Start](URL): First steps

## Core Concepts
- [Architecture](URL): System design
- [Components](URL): Building blocks

## API Reference
- [API Overview](URL): API introduction
- [Endpoints](URL): Available endpoints

## Optional
- [Advanced Topics](URL): Deep dives
- [Migration Guide](URL): Upgrading
```

**Key points**:
- Markdown format at `/llms.txt`
- Sections with H2 headers
- Links with optional descriptions
- "Optional" section for supplementary content

### sitemap.xml Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://docs.example.com/page1</loc>
    <lastmod>2026-01-15</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

**Sitemap Index** (for >50k URLs):
```xml
<sitemapindex>
  <sitemap>
    <loc>https://docs.example.com/sitemap-docs.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://docs.example.com/sitemap-api.xml</loc>
  </sitemap>
</sitemapindex>
```

## Comparison: Old vs New Approach

| Aspect | v0.1.0 (Old) | v0.2.0 (New) | Improvement |
|--------|--------------|--------------|-------------|
| **Collection time** | 15-20 min | 1-5 min | 75-90% faster |
| **Coverage** | 70-90% | 90-100% | +20-30% |
| **Methods** | WebFetch + WebSearch only | llms.txt + sitemap.xml + category strategies | +4 methods |
| **Automation** | Manual navigation | Standards-based auto-discovery | High |
| **Cost** | Free | Free | Same |
| **Reliability** | Medium | High | Improved |

## Quick Reference Card

### Phase 0: Resource Discovery
1. Check llms.txt → 95-100% coverage, 1 min
2. Check sitemap.xml → 90-100% coverage, 3 min
3. Determine category (GitHub OSS / Enterprise / API)
4. Select optimal strategy

### Phase 1: Category-Specific Collection (if Phase 0 insufficient)
- **Strategy A (GitHub OSS)**: DeepWiki + GitHub Pages + docs site
- **Strategy B (Enterprise/SaaS)**: WebFetch + WebSearch
- **Strategy C (API)**: OpenAPI spec + docs site
- **Fallback**: Traditional WebFetch + WebSearch

### Phase 2: Content Sampling
- Sample 5-10 pages
- Categorize and rate importance
- Mark essential pages with 🔥

### Phase 3: Repository Verification (GitHub projects only)
- Verify exact repo name with DeepWiki
- Document similar repos if confusion risk

### Phase 4: Command File Creation
- Use template from `references/template.md`
- Write entirely in Japanese
- Include 3-5 concrete WebFetch examples
- Document collection method used

### Phase 5: Quality Assurance
- Run coverage verification
- Complete self-check checklist
- Test URLs and DeepWiki access
- Confirm ambiguous points with user

## Additional Resources

### Template

See **`references/template.md`** for the complete command file template structure.

### Examples

See **`examples/haystack-example.md`** for a real-world example created with v0.1.0 workflow. Future examples will demonstrate v0.2.0 methods.

## Success Criteria

A well-created documentation command enables:
- ✅ 90-100% URL coverage using modern standards
- ✅ 1-5 minute collection time (vs 15-20 minutes before)
- ✅ Immediate access to common information via WebFetch
- ✅ Deeper understanding via DeepWiki when needed
- ✅ Source code investigation via Repomix as last resort
- ✅ Efficient token usage through progressive access
- ✅ Easy maintenance via documented collection method

Follow this modern workflow to create knowledge pathfinders efficiently without expensive crawling services or manual URL hunting.

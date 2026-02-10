# [Library Name] ドキュメント参照コマンド

## 概要

[ライブラリの簡潔な説明 - 1-2文で、何のためのライブラリか、主な特徴は何かを記述]

例:
- Haystackは、本番環境対応のAIエージェント、強力なRAGアプリケーション、スケーラブルなマルチモーダル検索システムを構築するためのオープンソースAIフレームワークです。
- Next.jsは、Reactベースのフルスタックフレームワークで、サーバーサイドレンダリング、静的サイト生成、APIルートなどの機能を提供します。

## 重要: [Similar Library] との違い

[混同しやすいライブラリがある場合、明確に区別する。ない場合はこのセクションを削除]

例:
- AI SDK (vercel/ai) は LLM 統合ライブラリ、AI Elements (vercel/ai-elements) は UI コンポーネント集
- Playwright (microsoft/playwright) はE2Eテストツール、Stagehand (browserbase/stagehand) はAIエージェント用ブラウザ制御

## ドキュメント構造

### 1. Getting Started
- **Introduction** 🔥: https://... - [簡潔な説明]
- **Installation**: https://... - [簡潔な説明]
- **Quick Start**: https://... - [簡潔な説明]

### 2. Core Concepts
- **Concept 1** 🔥: https://... - [簡潔な説明]
- **Concept 2**: https://... - [簡潔な説明]

### 3. Components / API Reference
- **Component Type 1** 🔥: https://... - [簡潔な説明]
- **Component Type 2**: https://... - [簡潔な説明]

### 4. Advanced Topics
- **Topic 1**: https://... - [簡潔な説明]
- **Topic 2**: https://... - [簡潔な説明]

### 5. [Additional Sections as needed]

[必要に応じてセクションを追加: Configuration, Deployment, Testing, etc.]

## ドキュメントへのアクセス方法

### 方法1: WebFetch（公式ドキュメント）- 最優先

最新情報と使用例の確認に最適。最初に試すべき方法。

#### 利用可能なドキュメントページ

**Getting Started:**
- `https://docs.example.com/intro` - イントロダクション
- `https://docs.example.com/installation` - インストール手順
- `https://docs.example.com/quick-start` - クイックスタート

**Core Concepts:**
- `https://docs.example.com/concepts/overview` - 概要
- `https://docs.example.com/concepts/architecture` - アーキテクチャ

**Components/API:**
- `https://docs.example.com/components` - コンポーネント一覧
- `https://docs.example.com/api-reference` - APIリファレンス

[実際のURLとセクションで置き換える]

#### 使用例

```typescript
// 例1: 基本的な使い方を学ぶ
WebFetch({
  url: "https://docs.example.com/quick-start",
  prompt: "[ライブラリ名]の基本的な使い方とセットアップ手順を詳しく教えてください"
})

// 例2: 特定のコンポーネント/機能について調べる
WebFetch({
  url: "https://docs.example.com/components/button",
  prompt: "Buttonコンポーネントの初期化方法、プロパティ、使用例を教えてください"
})

// 例3: アーキテクチャを理解する
WebFetch({
  url: "https://docs.example.com/concepts/architecture",
  prompt: "[ライブラリ名]のアーキテクチャと主要なコンセプトを説明してください"
})

// 例4: 設定方法を確認
WebFetch({
  url: "https://docs.example.com/configuration",
  prompt: "本番環境での推奨設定と注意点を教えてください"
})

// 例5: 実装例を見る
WebFetch({
  url: "https://docs.example.com/examples/[specific-example]",
  prompt: "[具体的なユースケース]の実装方法とベストプラクティスを教えてください"
})
```

[実際のユースケースに合わせて例を調整]

### 方法2: DeepWiki MCP（アーキテクチャと実装詳細）

**重要**: `[正確なリポジトリ名]` を指定してください（`[間違いやすいリポジトリ名]` ではありません）

WebFetchで十分な情報が得られなかった場合に使用。

```typescript
// リポジトリ構造の確認
mcp__deepwiki__read_wiki_structure({
  repoName: "org/repo-name"  // 注意: 正確なリポジトリ名
})

// 特定のトピックについて質問（日本語で質問すること）
mcp__deepwiki__ask_question({
  repoName: "org/repo-name",
  question: "[アーキテクチャや実装の詳細についての質問]"
})
```

#### DeepWikiで利用可能な情報

[実際に確認した目次構造を記載]

例:
- **Overview** - プロジェクト全体の概要
- **Architecture** - コアアーキテクチャ
- **Components** - コンポーネントシステム
- **Integration** - 外部統合
- **Advanced Features** - 高度な機能

#### DeepWikiが役立つケース

- コンポーネント間の連携メカニズムを理解したい
- 内部実装の詳細を知りたい
- アーキテクチャを深く理解したい
- カスタム拡張の実装方法を学びたい
- 特定の機能の内部動作を確認したい

### 方法3: Repomix MCP（ソースコード直接参照）- 最終手段

**重要**: `[正確なリポジトリ名]` を指定してください

トークン消費量が大きいため、他の方法で解決できない場合のみ使用。

```typescript
// 特定ファイルのみ取得（推奨）
mcp__repomix__pack_remote_repository({
  remote: "org/repo-name",
  includePatterns: "src/core/component.ts,src/utils/helper.ts",
  style: "xml"
})
```

#### Repomixが役立つケース

- ドキュメントに記載されていない実装の詳細を確認したい
- 特定のバグや問題を調査している
- ソースコードレベルでの理解が必要

## 推奨アプローチ

実際の使用時は、以下の順序でアクセス方法を試すことを推奨:

### レベル1: WebFetch（最優先）
- 基本的な使い方の確認
- コンポーネント/APIの仕様確認
- 実装例とベストプラクティス
- チュートリアルとクイックスタート

### レベル2: DeepWiki MCP（中程度の詳細度）
- アーキテクチャの理解
- 内部実装の詳細
- コンポーネント間の連携
- カスタム拡張開発

### レベル3: Repomix MCP（最も詳細、最終手段）
- ソースコード確認
- バグ調査
- ドキュメント化されていない挙動の確認

## クイックリファレンス

### [主要なユースケース1]
1. WebFetch: `https://docs.example.com/[relevant-page]`
2. [追加の推奨リソース]

### [主要なユースケース2]
1. WebFetch: `https://docs.example.com/[relevant-page]`
2. [追加の推奨リソース]

### [主要なユースケース3]
1. WebFetch: `https://docs.example.com/[relevant-page]`
2. [追加の推奨リソース]

[実際の主要ユースケースで置き換える]

## トラブルシューティング

### よくある問題1: [具体的な問題]
- **確認事項**: [チェックすべきこと]
- **対処法**: WebFetch `https://docs.example.com/[relevant-troubleshooting-page]`

### よくある問題2: [具体的な問題]
- **確認事項**: [チェックすべきこと]
- **対処法**: [具体的な解決手順]

[実際のよくある問題で置き換える。最大3-4個程度]

## 関連コマンド

他の類似コマンドと同じパターンで情報にアクセスできます:
- `/[related-library-1]`: [簡潔な説明]
- `/[related-library-2]`: [簡潔な説明]

[関連するライブラリのコマンドがあれば記載]

---

## テンプレート使用のヒント

### 必須セクション
- 概要
- ドキュメント構造
- アクセス方法（方法1-3）
- 推奨アプローチ

### オプションセクション
- 重要: [Similar Library] との違い（混同の恐れがある場合のみ）
- クイックリファレンス（主要ユースケースが明確な場合）
- トラブルシューティング（よくある問題がある場合）
- 関連コマンド（関連リソースがある場合）

### 重要度マーク（🔥）の使用基準
以下のいずれかに該当するページに付ける:
- 初心者が最初に読むべきページ
- 最も頻繁に参照されるページ
- 重要な概念やアーキテクチャを説明するページ
- 実装時に必須の情報が含まれるページ

1つのセクション内で1-3個程度に抑える（多すぎると意味がなくなる）

### URL数の目安
- 小規模ライブラリ: 20-40 URLs
- 中規模ライブラリ: 40-80 URLs
- 大規模ライブラリ: 80-150 URLs

多すぎる場合は、主要なページに絞るか、カテゴリを階層化する

### WebFetch例の数
- 最低3個、推奨5個
- 実際のユースケースをカバー
- 具体的なpromptを記載
- コピー&ペーストで使えるようにする

# Custom Code Review Plugin

多観点コードレビュープラグイン - 39の専門的なレビュー観点を活用した包括的なコードレビュー

## 概要

このプラグインは、39個の体系化されたコードレビュー観点を使用して、PRや変更内容を多角的にレビューします。セキュリティ、正確性、設計、テスト、パフォーマンスなど、様々な視点から網羅的なフィードバックを提供します。

### 特徴

- **39の専門観点**: セキュリティから設計パターンまで体系的にカバー
- **5つのレビューモード**: Light → Standard → Thorough で柔軟に選択
- **並列エージェント実行**: 複数の観点を同時にレビューして効率化
- **偽陽性チェック**: 自動検証で誤報を削減
- **プロジェクト別カスタマイズ**: `.local.md`で観点の追加/除外が可能
- **仕様設計支援スキル**: コード品質ガイドとして仕様決定時にも活用可能

## インストール

```bash
# marketplace.jsonに登録されている場合
cc plugins install custom-code-review

# またはローカルから
cc plugins link /path/to/custom-code-review
```

## 使い方

### 基本的な使い方

```bash
# 標準モード（推奨）
/custom-code-review:review

# クイックレビュー（5-10分）
/custom-code-review:review light

# 高速で包括的（10-15分）
/custom-code-review:review standard-fast

# 徹底的なレビュー（25-30分）
/custom-code-review:review thorough
```

### レビューモード

| モード | 観点数 | エージェント数 | 実行時間 | 用途 |
|--------|--------|--------------|---------|------|
| **Light** | 3-5 | 3-5 | ~5-10分 | 軽微な変更、クイックチェック |
| **Standard** | 7-10 | 7-10 | ~15-20分 | 通常のPR、機能開発 |
| **Standard Fast** | 7-10 | 3-4 | ~10-15分 | 高速かつ包括的 |
| **Thorough** | 15-20 | 15-20 | ~25-30分 | 重要な機能、セキュリティ |
| **Thorough Fast** | 15-20 | 5-7 | ~15-20分 | 包括的かつ効率的 |

### レビュー観点カテゴリ

1. **プロジェクト標準** (2観点): CLAUDE.md準拠、既存パターンとの整合性
2. **正確性** (5観点): バグ検出、エッジケース、例外安全性
3. **セキュリティ基本** (4観点): 基本的な脆弱性、共通パターン
4. **セキュリティ高度** (6観点): 攻撃者モデリング、ブラストラジアス分析
5. **テスト** (5観点): カバレッジ、品質、リグレッションテスト
6. **品質** (5観点): 読みやすさ、複雑度、コードスメル
7. **設計** (6観点): 型設計、APIデザイン、アーキテクチャパターン
8. **ドキュメント** (2観点): コメント品質、ドキュメント一貫性
9. **パフォーマンス** (3観点): パフォーマンス、アクセシビリティ、リソース管理
10. **コンテキスト** (2観点): Git履歴分析、コードベース理解

## プロジェクト別設定

プロジェクトルートに `.claude/custom-code-review.local.md` を作成してカスタマイズできます。

### 設定ファイルテンプレート

```markdown
---
mode: standard  # デフォルトモード
language: ja    # レポート言語（ja: 日本語, en: 英語, pt: ポルトガル語など）
excluded_perspectives:
  - DOC01  # コメント品質チェックをスキップ
  - PERF02 # アクセシビリティをスキップ
max_parallel_agents: 7
---

# Additional Instructions

このプロジェクトではReact Hooksのルールを厳守してください。
```

### 設定項目

**YAML Frontmatter**:
- `mode`: デフォルトのレビューモード
- `language`: レポート出力言語（デフォルト: `ja`）
  - `ja`: 日本語
  - `en`: 英語
  - `pt`: ポルトガル語
  - その他の言語コードも指定可能
- `excluded_perspectives`: 除外する観点ID（配列）
- `max_parallel_agents`: 並列エージェント数の上限

**Markdown本文**:
- レビューエージェントへの追加指示
- 言語指定、プロジェクト固有ルールなど

## レビューフロー

1. **PR情報収集**: git diff、コミットメッセージ、関連ファイルを収集
2. **モード選択**: 5つのモードから選択（インタラクティブ）
3. **並列レビュー**: 複数の観点エージェントが同時にレビュー
4. **統合**: 重複した指摘を排除して1つのレポートに
5. **検証**: 偽陽性の可能性がある指摘を再検証
6. **結果提示**: 優先度別に整理された結果を表示

## 出力ファイル

レビュー結果は `/tmp/claude-code-review-{session-id}/` に保存されます。

- **verified.md**: 最終レビューレポート（偽陽性チェック済み）
- **consolidated.md**: 統合レポート（重複排除済み）
- **pr-summary.md**: PR情報サマリー
- **reviews/perspective-*.md**: 各観点の個別レビュー

## 仕様設計支援スキル

コードレビューだけでなく、仕様決定やアーキテクチャ設計時にも活用できます。

### perspective-guide スキル

```
「良いコードとは何か知りたい」
「新しいAPIの設計で考慮すべき観点は？」
「認証機能の仕様を決めたい」
```

このようなリクエストで、自動的にスキルが起動し、39の観点から関連する情報を提供します。

**手動起動**:
```
/custom-code-review:perspective-guide
```

**できること**:
- INDEX.mdで全体像を把握
- 興味のあるカテゴリの観点を深掘り
- 仕様決定時のチェックリスト作成
- ベストプラクティスの参照

## よくある質問

### Q: レビューに時間がかかりすぎる
**A**: `standard-fast` または `light` モードを使用してください。Fastモードは複数の観点を1エージェントにまとめて高速化します。

### Q: 特定の観点だけをレビューしたい
**A**: `.local.md`で不要な観点を`excluded_perspectives`に追加してください。

### Q: 偽陽性が多い
**A**: Verifierエージェントが自動で偽陽性をチェックしますが、`verified.md`の「Needs User Verification」セクションで最終確認してください。

### Q: 独自の観点を追加したい
**A**: 将来のバージョンで対応予定です。現在は既存の39観点のみ使用可能です。

## トラブルシューティング

### エージェントが起動しない
- Gitリポジトリ内で実行していることを確認
- 変更があることを確認（`git status`）

### 設定ファイルが読み込まれない
- ファイルパスを確認: `.claude/custom-code-review.local.md`
- YAMLフロントマターの文法をチェック

### レビュー結果が見つからない
- セッションIDを確認: `/tmp/claude-code-review-{session-id}/`
- コマンド実行後に表示されるパスをコピー

## 開発

### ディレクトリ構造

```
custom-code-review/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── review.md
├── agents/
│   ├── pr-analyzer.md
│   ├── perspective-reviewer.md
│   ├── consolidator.md
│   └── verifier.md
├── skills/
│   └── perspective-guide/
│       └── SKILL.md
├── references/
│   └── perspectives/
│       ├── INDEX.md
│       ├── project-standards/
│       ├── correctness/
│       ├── security-basic/
│       ├── security-advanced/
│       ├── testing/
│       ├── quality/
│       ├── design/
│       ├── documentation/
│       ├── performance/
│       └── context/
└── README.md
```

### エージェント構成

- **pr-analyzer** (Sonnet): PR情報収集
- **perspective-reviewer** (Sonnet): 汎用レビューエージェント（複数インスタンス起動）
- **consolidator** (Haiku): 重複排除
- **verifier** (Sonnet): 偽陽性チェック

### 信頼度スコア

- **91-100**: Critical - 確実に問題
- **80-90**: Important - 高確率で問題
- **80未満**: レポートしない（偽陽性の可能性）

## ライセンス

MIT

## 作者

tyo-yo

## 変更履歴

### 1.0.0 (2026-02-11)
- 初回リリース
- 39の観点によるマルチパースペクティブレビュー
- 5つのレビューモード（Light, Standard, Standard Fast, Thorough, Thorough Fast）
- 偽陽性チェック機能
- プロジェクト別カスタマイズ
- 仕様設計支援スキル（perspective-guide）

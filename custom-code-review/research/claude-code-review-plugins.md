# Claude Code コードレビュー関連プラグイン徹底調査

調査日: 2026-02-10

## 目次

1. [公式プラグイン](#公式プラグイン)
   - [PR Review Toolkit](#1-pr-review-toolkit)
   - [Feature Dev](#2-feature-dev)
   - [Code Review](#3-code-review)
2. [コミュニティプラグイン](#コミュニティプラグイン)
   - [matsengrp/plugins](#1-matsengrpplugins)
   - [anilcancakir/claude-code-plugins](#2-anilcancakirclaude-code-plugins)
3. [レビュー観点の比較分析](#レビュー観点の比較分析)
4. [プロンプト設計パターン](#プロンプト設計パターン)
5. [参考リンク](#参考リンク)

---

## 公式プラグイン

### 1. PR Review Toolkit

**リポジトリ**: [anthropics/claude-code/plugins/pr-review-toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)

#### 概要
プルリクエストの徹底的なレビューのための6つの専門的なエージェントを統合したプラグイン。各エージェントが異なる観点から品質をチェックする。

#### ディレクトリ構造
```
plugins/pr-review-toolkit/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── code-reviewer.md
│   ├── comment-analyzer.md
│   ├── pr-test-analyzer.md
│   ├── silent-failure-hunter.md
│   ├── type-design-analyzer.md
│   └── code-simplifier.md
├── commands/
│   └── review-pr.md
└── README.md
```

#### 6つのエージェント

##### 1.1 code-reviewer

**目的**: プロジェクトガイドラインへの準拠、バグ検出、コード品質を確認

**使用タイミング**:
- 機能実装後の検証
- コード作成直後のプロアクティブなレビュー
- PR作成前の品質確認

**レビュー観点**:

| 観点 | 詳細 |
|------|------|
| プロジェクトガイドライン準拠 | CLAUDE.mdの明示的ルール（インポートパターン、フレームワーク規則、スタイル、命名規則など）を検証 |
| バグ検出 | 機能に影響するロジックエラー、null処理、セキュリティ脆弱性、パフォーマンス問題を特定 |
| コード品質 | 重大な重複、不足した例外処理、アクセシビリティ問題などを評価 |

**信頼度スコアリング**:
- 0-25点: 誤検知の可能性
- 26-50点: 軽微な指摘
- 51-75点: 低影響の問題
- 76-90点: 注目すべき問題
- 91-100点: 致命的なバグまたは明示的な違反

**報告基準**: 80点以上のみ報告

**出力形式**:
```markdown
## Code Review Results

### Critical Issues (91-100)
1. [説明]
   - Confidence: [スコア]
   - File: [ファイルパス:行番号]
   - Guideline: [CLAUDE.md参照]
   - Fix: [修正提案]

### Important Issues (80-89)
...
```

**プロンプトの特徴**:
- 信頼度ベースのフィルタリングで誤検知を削減
- CLAUDE.mdへの明示的参照を強制
- ファイルパス:行番号の具体的な位置指定

##### 1.2 comment-analyzer

**目的**: コード内のコメント精度、完全性、長期保守性を分析

**使用タイミング**:
- 大規模なドキュメンテーションコメント生成後の検証
- プルリクエスト前のコメント確認
- 既存コメントの技術的負債や陳腐化の確認
- コメントと実装の正確性検証

**5つのレビュー観点**:

| 観点 | 詳細 |
|------|------|
| 事実検証 | 署名、戻り値、型参照、エッジケース対応が実装と一致するか確認 |
| 完全性評価 | 前提条件、副作用、エラー処理、複雑なアルゴリズムの説明が網羅されているか |
| 長期価値評価 | 「自明なコードを繰り返すだけのコメント」は削除対象。「なぜ」の説明を重視 |
| 誤解要因の特定 | 曖昧性、古い参照、対応しない仮定、矛盾する例を検出 |
| 改善提案 | 具体的で実行可能なフィードバックを提供 |

**出力フォーマット**:
```markdown
## Comment Analysis

### Overview
[分析範囲と主要所見]

### Critical Issues
[不正確または誤解招く箇所]

### Improvement Opportunities
[強化可能な部分]

### Candidates for Removal
[不要なコメント]

### Good Examples
[参考になるコメント例]
```

**プロンプトの特徴**:
- 「自明なコメント」の削除を積極的に提案
- 「なぜ」の説明を重視する哲学
- 長期保守者の視点を重視

##### 1.3 pr-test-analyzer

**目的**: テストカバレッジの品質と完全性を評価（行カバレッジではなく振る舞いカバレッジ）

**使用タイミング**:
- PR作成直後のテスト徹底性確認
- PR更新後の新機能のカバレッジ検証
- マージ前の最終的なテストカバレッジチェック

**主要なレビュー観点**:

| 観点 | 詳細 |
|------|------|
| エラーハンドリングパスの未テスト | 例外処理が適切にテストされているか |
| 境界値などのエッジケース | 境界条件、null、空配列、極端な値のテスト |
| ビジネスロジック分岐の未カバー | 重要なif文や条件分岐のカバレッジ |
| 検証ロジックの負のテストケース | 失敗ケースが適切にテストされているか |
| テスト品質評価 | 実装詳細ではなく振る舞いをテストしているか |

**重大度レーティング**:
- 9-10点: データ喪失やセキュリティ問題につながる重大機能
- 5-8点: ユーザーに影響する重要なロジック～軽微な問題
- 1-4点: 補完的・オプショナルなカバレッジ

**出力フォーマット**:
```markdown
## Test Coverage Analysis

### Overview
[分析概要]

### Critical Gaps (8-10)
1. [未カバー項目]
   - Severity: [スコア]
   - Location: [ファイルパス:行番号]
   - Risk: [リスク説明]

### Important Improvements (5-7)
...

### Test Quality Issues
[テスト品質の問題点]

### Positive Observations
[良好なテスト例]
```

**プロンプトの特徴**:
- 「行カバレッジ」ではなく「振る舞いカバレッジ」を重視
- リファクタリング後も有効なテストかを判断
- 「メトリクス達成」ではなく「実際のバグ予防」に重点

##### 1.4 silent-failure-hunter

**目的**: エラーハンドリングの不備、不適切なフォールバック、エラー抑制を検出

**使用タイミング**:
- APIクライアントにフォールバック機能を実装した後
- プルリクエストにtry-catchブロックが含まれている場合
- エラーハンドリングコードをリファクタリング後

**核心原則（5項目）**:

| 原則 | 詳細 |
|------|------|
| サイレントエラーは許容不可 | ログと通知なしのエラーは致命的欠陥 |
| ユーザーへのアクション可能なフィードバック | 何が起きたか、どう対応するかを明確に |
| フォールバックは明確かつ正当化される必要 | ユーザー認識なしの代替動作は問題隠蔽 |
| キャッチブロックは限定的であること | 広すぎる例外捕捉は無関係エラーを隠す |
| モック実装はテストのみ | 本番コードのモック使用は設計の問題 |

**レビュープロセス（5段階）**:

1. **エラーハンドリングコード特定**
   - try-catchブロック、エラーコールバック、条件分岐、フォールバック、ログ続行処理を検出

2. **各エラーハンドリアの精査**
   - ログ品質: 適切な重大度、充分なコンテキスト、エラーID、保守性
   - ユーザーフィードバック: 明確性、実行可能性、具体性、技術詳細の適切な露出
   - キャッチ特異性: 予期されたエラー型のみ、潜在的に隠されるエラー分析
   - フォールバック動作: ユーザー明示要求、問題マスキング、混乱可能性、テスト外のモック
   - エラー伝播: より高次なハンドラへの委譲判定、吸収の是非

3. **エラーメッセージ検査**
   - 表現明瞭性、根本原因説明、対応策、専門用語適切性、コンテキスト

4. **隠れたエラー検出**
   - 空のキャッチ、ログのみで継続、無言の初期値返却、静的フォールバック、説明なし再試行

5. **プロジェクト標準検証**
   - 本番コード沈黙禁止、必須ログ記録、エラーID使用、適切伝播

**出力フォーマット**:
```markdown
## Silent Failure Analysis

### Critical Issues
1. [問題説明]
   - Location: [ファイルパス:行番号]
   - Severity: CRITICAL/HIGH/MEDIUM
   - What could go wrong: [潜在エラー]
   - User impact: [ユーザー影響]
   - Recommendation: [推奨対応]
   - Fix example: [修正例]
```

**プロンプトの特徴**:
- 徹底的、懐疑的、非妥協的な姿勢
- デバッグの悪夢と解決策を具体的に指摘
- エラーハンドリングに特化した専門性

##### 1.5 type-design-analyzer

**目的**: 型設計の品質と不変性（invariants）の表現を評価

**使用タイミング**:
- 新しい型導入時
- プルリクエスト作成時（全ての型をレビュー）
- 型リファクタリング時

**コア分析フレームワーク（4段階）**:

| 段階 | 詳細 |
|------|------|
| イテラント識別 | データ一貫性、状態遷移、フィールド関係制約、ビジネスロール抽出 |
| カプセル化評価（1-10） | 内部実装隠蔽、外部からの違反可能性、アクセス修飾子の適切性 |
| イテラント表現評価（1-10） | 構造による明確性、コンパイル時強制可能性、自己説明性 |
| イテラント有用性評価（1-10） | 実バグ防止性、ビジネス要件適合性、推論容易性 |

**出力フォーマット**:
```markdown
## Type Design Analysis

### Type: [型名]

**Identified Invariants:**
- [不変性リスト]

**Ratings:**
- Encapsulation: [1-10] - [根拠]
- Invariant Expression: [1-10] - [根拠]
- Invariant Usefulness: [1-10] - [根拠]

**Strengths:**
- [強み]

**Concerns:**
- [懸念事項]

**Improvement Suggestions:**
- [改善提案]
```

**プロンプトの特徴**:
- 「ランタイムチェックよりコンパイル時の保証を優先」する設計哲学
- 複雑さとのバランスを考慮した実用的改善
- TypeScript/型安全言語に特化

##### 1.6 code-simplifier

**目的**: 機能を保持しながらコードの明確性、一貫性、保守性を向上

**使用タイミング**:
- コードが作成・修正された後（自動起動）
- 認証実装、バグ修正、パフォーマンス最適化などの論理的なコードチャンク完成後

**レビュー観点**:

| 観点 | 詳細 |
|------|------|
| 機能保持 | 動作を変えない |
| プロジェクト標準準拠 | ESモジュール、function キーワード優先、明示的な型注釈 |
| 明確性向上 | 不要な複雑さ削減、ネストされた三項演算子を避ける |
| バランス維持 | 過度な単純化を避け、保守性を損なわない |
| 焦点範囲 | 最近修正されたコードセクションのみが対象 |

**重要方針**:
- 「明示的コードは簡潔さより優先」
- ネストされた三項演算子をswitch/if-elseに置き換え
- 可読性を重視

**出力フォーマット**:
```markdown
## Simplification Suggestions

### Section: [コードセクション]

**Current Issues:**
- [複雑性の問題]

**Suggested Refactoring:**
```typescript
// Before
[元のコード]

// After
[簡潔化されたコード]
```

**Rationale:**
[理由説明]
```

**プロンプトの特徴**:
- コードチャンク完成後に自動実行
- 機能保持を最優先
- プロジェクト標準への準拠

#### 推奨ワークフロー

```
1. コード作成 → code-reviewer
2. 修正 → silent-failure-hunter（エラーハンドリング修正時）
3. テスト追加 → pr-test-analyzer
4. ドキュメント追加 → comment-analyzer
5. PR作成前 → 必要に応じて複数エージェント実行
6. レビュー合格後 → code-simplifier（ポーランド）
```

#### 使用方法

```bash
# インストール
/plugins
# 「pr-review-toolkit」を検索してインストール

# 個別エージェント使用
"テストがすべてのエッジケースをカバーしていますか?"  # pr-test-analyzer トリガー

# 包括的なPRレビュー
"このPRを作成する準備ができました。以下をお願いします:
1. テストカバレッジをレビュー
2. 静かな失敗をチェック
3. コメントの精度を確認
4. 新しい型をレビュー
5. 一般的なコードレビュー"
```

---

### 2. Feature Dev

**リポジトリ**: [anthropics/claude-code/plugins/feature-dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)

#### 概要
包括的な機能開発ワークフロープラグイン。7段階のフェーズで新機能を体系的に開発。

#### ディレクトリ構造
```
plugins/feature-dev/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── code-explorer.md
│   ├── code-architect.md
│   └── code-reviewer.md
├── commands/
│   └── feature-dev.md
└── README.md
```

#### 7段階のワークフロー

| フェーズ | 名称 | 目的 |
|---------|------|------|
| 1 | Discovery（発見） | 構築内容の理解を明確化 |
| 2 | Codebase Exploration | 既存コード・パターンの理解 |
| 3 | Clarifying Questions | 曖昧性の排除と要件確認 |
| 4 | Architecture Design | 実装アプローチの設計 |
| 5 | Implementation | 機能の実装 |
| 6 | Quality Review | コード品質とバグチェック |
| 7 | Summary | 実装完了の記録 |

#### 3つのエージェント

##### 2.1 code-explorer

**目的**: 既存コードベースの深掘り分析

**実行時期**: フェーズ2（自動実行）または手動実行

**焦点領域**:
- エントリーポイントと呼び出しチェーン
- データフローと変換
- アーキテクチャレイヤーとパターン
- 依存性と統合
- 実装の詳細

**分析観点（4段階）**:

| 段階 | 詳細 |
|------|------|
| 機能発見 | APIやUIコンポーネント、CLIコマンドなどの入口特定<br>主要実装ファイルの特定<br>機能範囲と設定のマッピング |
| コードフロー追跡 | エントリーポイントから出力までの呼び出しチェーンを追跡<br>各ステップでのデータ変換を追跡<br>すべての依存関係と統合を識別<br>状態変化と副作用を文書化 |
| アーキテクチャ分析 | プレゼンテーション→ビジネスロジック→データの層構造<br>設計パターンと建築的決定の識別<br>コンポーネント間のインターフェース<br>横断的関心事（認証、ログ、キャッシング） |
| 実装詳細 | アルゴリズムとデータ構造<br>エラー処理とエッジケース<br>パフォーマンス配慮<br>技術債と改善機会 |

**出力内容**:
- 実装トレース（ファイル:行番号参照付き）
- ステップバイステップの実行フロー
- 主要コンポーネントと責務
- アーキテクチャインサイト
- 読むべき必須ファイルのリスト

**プロンプトの特徴**:
- ファイルパスと行番号の具体的参照を含む
- 入口から出口まで完全な実行パスをトレース
- 既存パターンの理解を重視

##### 2.2 code-architect

**目的**: 機能アーキテクチャと実装ブループリントの設計

**実行時期**: フェーズ4（自動実行）または手動実行

**焦点領域**:
- コードベースパターン分析
- アーキテクチャ決定
- コンポーネント設計
- 実装ロードマップ
- データフローとビルドシーケンス

**核心プロセス**:

1. **コードベース分析**
   - 技術スタック、モジュール境界、抽象化レイヤーを抽出
   - 既存の慣例とガイドラインを確認
   - 類似機能を特定

2. **アーキテクチャ設計**
   - 複数案検討ではなく、「一つのアプローチを選択し実行」という決断的姿勢
   - 既存コードへの統合性を確保
   - テスト性と保守性を重視

3. **完全な実装ブループリント提供**
   - 各ファイルの作成・修正内容
   - コンポーネント責務
   - 統合点
   - データフロー
   - 実装フェーズをチェックリスト化

**設計アプローチ（3種類）**:

| アプローチ | 特徴 |
|-----------|------|
| 最小限の変更 | 最速、最低リスク |
| クリーンアーキテクチャ | 保守性と優雅さを重視 |
| プラグマティックバランス | 速度と品質のバランス |

**出力内容**:
- 発見されたパターンと規約（ファイル:行番号参照付き）
- 根拠付きのアーキテクチャ決定
- 完全なコンポーネント設計（責務・依存関係・インターフェース）
- 特定ファイルを含む実装マップ
- データフロー図
- 段階的なビルドシーケンス
- エラー処理、状態管理、セキュリティ考慮事項

**プロンプトの特徴**:
- 曖昧性を避け、ファイルパス・関数名など具体的で実行可能な指示
- 決断的姿勢（複数案を提示せず、一つを選択）
- 既存パターンへの適合を重視

##### 2.3 code-reviewer (Feature-Dev版)

**目的**: バグ、論理エラー、セキュリティ脆弱性、コード品質問題をレビュー

**実行時期**: フェーズ6（自動実行）または手動実行

**レビュー観点**:

| 観点 | 詳細 |
|------|------|
| プロジェクトガイドライン準拠 | CLAUDE.mdで定義されたルール（インポート方式、フレームワーク規約、言語別スタイル、エラーハンドリング、ロギング、テスト慣行）を検証 |
| バグ検出 | ロジックエラー、null/undefined処理、競合状態、メモリリーク、セキュリティ脆弱性、パフォーマンス問題を特定 |
| コード品質 | コード重複、欠落したエラーハンドリング、アクセシビリティ、テストカバレッジを評価 |

**信頼度スコアリング**:

| スコア | 判定 |
|--------|------|
| 0-50 | 報告しない（誤検出またはニッチな指摘） |
| 75 | 高信頼度（実装上の問題が実際に発生する） |
| 100 | 確実（頻繁に起こる実問題） |

**報告基準**: 信頼度80以上のみ記載

**出力フォーマット**:
```markdown
## Quality Review

### Critical Issues
1. [説明]
   - Confidence: [スコア]
   - File: [ファイルパス:行番号]
   - Guideline: [CLAUDE.md参照]
   - Fix: [修正提案]

### Important Issues
...
```

**PR-Review-Toolkit版との主な違い**:
- より精密な「偽陽性最小化」を強調
- 「高優先度問題への特化」を重視
- Feature開発ワークフローに組み込まれた使用を想定

#### 使用方法

```bash
# 完全なワークフロー（推奨）
/feature-dev Add rate limiting to API endpoints

# 手動エージェント実行
"Launch code-explorer to trace how authentication works"
"Launch code-architect to design the caching layer"
"Launch code-reviewer to check my recent changes"
```

#### 使用シーン

**推奨される場合**:
- 複数ファイルに影響する新機能
- アーキテクチャ判断が必要な機能
- 既存コードとの複雑な統合
- 要件が不明確な機能

**不適切な場合**:
- 単一行のバグ修正
- 些細な変更
- よく定義された単純なタスク
- 緊急のホットフィックス

#### ベストプラクティス

1. 複雑な機能では完全なワークフローを使用
2. クラリファイング質問に思慮深く回答
3. アーキテクチャを意識的に選択
4. コードレビューをスキップしない
5. 提案されたファイルを読むことで文脈を習得

---

### 3. Code Review

**リポジトリ**: [anthropics/claude-code/plugins/code-review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)

#### 概要
複数の専門化されたエージェントを並列で起動し、信頼度スコアに基づいて誤検知をフィルタリングするプルリクエストの自動コードレビュー機能。

#### ディレクトリ構造
```
plugins/code-review/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── code-review.md
└── README.md
```

#### 含まれるエージェント（4つ）

| エージェント | 役割 |
|-------------|------|
| CLAUDE.md コンプライアンス監査エージェント #1 | ガイドラインの準拠状況を監査<br>CLAUDE.mdファイルの明示的な検証 |
| CLAUDE.md コンプライアンス監査エージェント #2 | CLAUDE.mdコンプライアンスの冗長性確保<br>複数の視点からのチェック |
| バグ検出エージェント | 変更内容の明らかなバグをスキャン<br>既存問題ではなく、PRで導入された問題に焦点 |
| 履歴分析エージェント | Gitブレーム/履歴からコンテキスト情報を分析<br>背景に基づくイシュー検出 |

#### 主要なコマンド

**コマンド**: `/code-review [--comment]`

**機能**:
1. レビュー必要性の確認（クローズ済み、ドラフト、自明、既レビューPRはスキップ）
2. CLAUDE.mdガイドラインファイルの収集
3. PR変更内容の要約
4. 4つのエージェントの並列実行
5. 信頼度スコア（0-100）の付与
6. 信頼度80以上のイシューのみを出力

**使用方法**:
```bash
# ターミナルに出力（デフォルト）
/code-review

# PRコメントとして投稿
/code-review --comment
```

#### 信頼度スコアリングシステム

| スコア | 意味 |
|--------|------|
| 0 | 信頼度なし、誤検知 |
| 25 | やや確実、実在の可能性 |
| 50 | 中程度の確実性、軽微な問題 |
| 75 | 高い確実性、重要な問題 |
| 100 | 絶対確実、確実に実在 |

**デフォルト閾値**: 80（設定で調整可能）

#### レビュー出力例

```markdown
## Code review

Found 3 issues:

1. Missing error handling for OAuth callback (CLAUDE.md says "Always handle OAuth errors")

https://github.com/owner/repo/blob/abc123.../src/auth.ts#L67-L72

2. Memory leak: OAuth state not cleaned up (bug due to missing cleanup in finally block)

https://github.com/owner/repo/blob/abc123.../src/auth.ts#L88-L95

3. Inconsistent naming pattern (src/conventions/CLAUDE.md says "Use camelCase for functions")

https://github.com/owner/repo/blob/abc123.../src/utils.ts#L23-L28
```

#### 必要要件

- Gitリポジトリと GitHub統合
- GitHub CLI（`gh`）のインストールと認証
- CLAUDE.mdファイル（推奨、ガイドラインチェック用）

#### 自動スキップ対象

- クローズ済みPR
- ドラフトPR
- 自明な自動PR
- 既にレビュー済みのPR

#### プロンプトの特徴

- 4つのエージェントによる並列レビュー
- CLAUDE.mdへの強い依存（2つのエージェントが専用）
- Git履歴を活用したコンテキスト分析
- 信頼度ベースの厳格なフィルタリング

---

## コミュニティプラグイン

### 1. matsengrp/plugins

**リポジトリ**: [matsengrp/plugins](https://github.com/matsengrp/plugins)

#### 概要
科学論文執筆、コードレビュー、技術ドキュメントに特化した専門エージェント。

#### コードレビュー関連の機能

**3つの主要なエージェント**:

| エージェント | 焦点 |
|-------------|------|
| clean-code-reviewer | クリーンコード原則に基づいた専門的なレビュー |
| code-smell-detector | コード臭の検出を「mentoring approach」で行う優しい指摘スタイル |
| antipattern-scanner | アーキテクチャ上の問題パターンを識別 |

#### スラッシュコマンド

**コマンド**: `/pre-pr-check`

**機能**:
- コード形式と文書化の検証
- 上述のエージェントによるアーキテクチャレビュー
- テスト品質の評価
- 静的解析ツール（ruff、mypy等）の実行

**特徴**:
- プルリクエスト作成前の品質基準確認に有用
- クリーンコード原則を重視
- メンタリングアプローチで教育的なフィードバック

---

### 2. anilcancakir/claude-code-plugins

**リポジトリ**: [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)

#### 概要
コンテキスト管理、コードレビュー、TDDワークフロー、市場調査、プロジェクト最適化を提供するマーケットプレイス。

#### Pre-Commit Flow プラグイン

**主要機能**:

| 機能 | 詳細 |
|------|------|
| Code Review | セキュリティ分析、バグ検出、品質チェック |
| Documentation | PHPDoc、DartDoc、JSDoc等のインラインドキュメント自動更新 |
| Smart Commits | コミットスタイル自動検出とセマンティックメッセージ生成 |
| Multi-Stack対応 | Laravel、Flutter、Vue、Nuxt、TailwindCSS、Alpine.js |

#### コマンド構成

| コマンド | 機能 |
|---------|------|
| `/my_review` | セキュリティ分析を含むコードレビュー実行 |
| `/my_docs` | インラインドキュメンテーション更新 |
| `/my_commit` | スマートコミットメッセージ生成 |
| `/my_send` | レビュー→ドキュメント→コミットの統合ワークフロー |

#### アーキテクチャ構成

```
pre-commit-flow/
├── hooks/           # ワークフロー定義
├── scripts/         # Shell実装スクリプト
└── skills/          # レビュー機能モジュール
```

**特徴**:
- エージェント方式ではなく、スキルベースの単一プラグイン設計
- 特定のスタック（Laravel、Flutter等）に特化
- ドキュメント生成とコミット生成を統合

---

## レビュー観点の比較分析

### 観点マトリクス

| レビュー観点 | PR Review Toolkit | Feature Dev | Code Review | matsengrp | anilcancakir |
|-------------|-------------------|-------------|-------------|-----------|-------------|
| **ガイドライン準拠** | ✅ (code-reviewer) | ✅ (code-reviewer) | ✅ (2エージェント) | - | - |
| **バグ検出** | ✅ (code-reviewer) | ✅ (code-reviewer) | ✅ (1エージェント) | - | ✅ (/my_review) |
| **セキュリティ** | ✅ (code-reviewer) | ✅ (code-reviewer) | - | - | ✅ (/my_review) |
| **テストカバレッジ** | ✅ (pr-test-analyzer) | - | - | ✅ (pre-pr-check) | - |
| **エラーハンドリング** | ✅ (silent-failure-hunter) | - | - | - | - |
| **コメント品質** | ✅ (comment-analyzer) | - | - | - | ✅ (/my_docs) |
| **型設計** | ✅ (type-design-analyzer) | - | - | - | - |
| **コード簡潔化** | ✅ (code-simplifier) | - | - | - | - |
| **クリーンコード原則** | - | - | - | ✅ (clean-code-reviewer) | - |
| **コード臭検出** | - | - | - | ✅ (code-smell-detector) | - |
| **アンチパターン検出** | - | - | - | ✅ (antipattern-scanner) | - |
| **Git履歴分析** | - | - | ✅ (1エージェント) | - | - |
| **アーキテクチャ分析** | - | ✅ (code-architect) | - | ✅ (antipattern-scanner) | - |
| **コードベース探索** | - | ✅ (code-explorer) | - | - | - |
| **信頼度スコアリング** | ✅ (80+) | ✅ (80+) | ✅ (80+) | - | - |

### 特化領域の比較

| プラグイン | 主な特化領域 |
|-----------|-------------|
| **PR Review Toolkit** | 包括的なPRレビュー（6つの専門エージェント）<br>テスト、エラーハンドリング、型設計、コメント品質など細分化 |
| **Feature Dev** | 機能開発ワークフロー<br>コードベース探索→設計→実装→レビューの一貫性 |
| **Code Review** | シンプルで高速なPRレビュー<br>CLAUDE.md準拠とバグ検出に特化 |
| **matsengrp** | クリーンコード原則<br>教育的・メンタリングアプローチ |
| **anilcancakir** | 特定スタック（Laravel、Flutter等）<br>ドキュメント生成とコミット生成の統合 |

---

## プロンプト設計パターン

### 1. 信頼度スコアリングパターン

**使用例**: PR Review Toolkit, Feature Dev, Code Review

**設計パターン**:
```markdown
## Confidence Scoring

Rate each issue on a 0-100 scale:
- 0-25: Likely false positive
- 26-50: Minor suggestion
- 51-75: Low impact issue
- 76-90: Notable problem
- 91-100: Critical bug or explicit violation

**Report only issues with confidence ≥ 80.**
```

**効果**:
- 誤検知の削減
- レビューノイズの最小化
- 高優先度問題への集中

**実装のポイント**:
- 閾値を明確に定義（デフォルト80）
- スコアリング基準を具体的に記述
- エージェントに「確信がない場合は報告しない」を徹底

### 2. ファイルパス参照パターン

**使用例**: 全てのプラグイン

**設計パターン**:
```markdown
For each issue, provide:
- File path: [path/to/file.ts:line_number]
- Specific line range: L67-L72
- GitHub permalink if available
```

**効果**:
- レビュー指摘の具体性向上
- 開発者が即座に該当箇所を特定可能
- PRコメントへの自動リンク化

**実装のポイント**:
- ファイルパス+行番号を必須化
- 行範囲を指定（単一行ではなく）
- GitHubのパーマリンク形式を推奨

### 3. CLAUDE.md準拠パターン

**使用例**: PR Review Toolkit, Feature Dev, Code Review

**設計パターン**:
```markdown
## Project Guidelines

1. Read CLAUDE.md in the repository root
2. For each guideline violation, cite the specific rule
3. Include the exact quote from CLAUDE.md

Format:
- Violation: [description]
- Guideline: "CLAUDE.md says: [exact quote]"
- Fix: [suggestion]
```

**効果**:
- プロジェクト固有ルールの徹底
- ガイドラインへの明示的な参照
- チーム内での一貫性確保

**実装のポイント**:
- CLAUDE.mdの読み込みを必須化
- 引用を含めることで説得力向上
- 「ガイドライン違反」と「一般的なベストプラクティス」を区別

### 4. 段階的分析パターン

**使用例**: silent-failure-hunter, code-explorer

**設計パターン**:
```markdown
## Analysis Process

1. **Identification**: Locate all error handling code
2. **Inspection**: Examine each handler for issues
3. **Message Review**: Check error message clarity
4. **Hidden Error Detection**: Find silent failures
5. **Standards Verification**: Check project standards
```

**効果**:
- 体系的で漏れのないレビュー
- 分析プロセスの透明性
- 再現可能な手法

**実装のポイント**:
- 各段階を明確に定義
- 段階ごとのチェックリストを提供
- 順序を守ることを強調

### 5. 複数エージェント並列実行パターン

**使用例**: Code Review

**設計パターン**:
```markdown
## Parallel Review Agents

Launch 4 agents in parallel:
1. CLAUDE.md Compliance Auditor #1
2. CLAUDE.md Compliance Auditor #2 (redundancy)
3. Bug Detector
4. Git History Analyzer

Aggregate results and filter by confidence ≥ 80.
```

**効果**:
- 異なる視点からの網羅的レビュー
- レビュー時間の短縮（並列処理）
- 冗長性による信頼性向上

**実装のポイント**:
- エージェント間の責務を明確に分離
- 結果の集約方法を定義
- 重複検出とマージのロジック

### 6. 教育的フィードバックパターン

**使用例**: matsengrp (code-smell-detector)

**設計パターン**:
```markdown
## Mentoring Approach

For each issue:
1. What: Identify the problem
2. Why: Explain why it's problematic
3. How: Provide concrete examples
4. Learn: Reference best practices or patterns

Tone: Constructive and educational, not critical.
```

**効果**:
- 開発者のスキル向上
- ポジティブなレビュー文化
- 長期的なコード品質改善

**実装のポイント**:
- トーンを明確に指定（"constructive", "gentle"）
- 問題だけでなく「なぜ」を説明
- 参考資料やベストプラクティスへのリンク

### 7. 振る舞いカバレッジパターン

**使用例**: pr-test-analyzer

**設計パターン**:
```markdown
## Behavior Coverage vs Line Coverage

Focus on:
- Does the test verify behavior, not implementation?
- Will the test remain valid after refactoring?
- Does it catch real bugs users would experience?

NOT:
- Line coverage percentage
- Testing implementation details
- Trivial getters/setters
```

**効果**:
- 実用的なテストの推奨
- メトリクス至上主義の回避
- リファクタリング耐性のあるテスト

**実装のポイント**:
- 「行カバレッジ」と明確に区別
- 「振る舞い」の定義を具体化
- 実装詳細テストの例を示す

### 8. 決断的設計パターン

**使用例**: code-architect

**設計パターン**:
```markdown
## Decisive Architecture

Do NOT:
- Present multiple options
- Say "you could do X or Y"
- Leave decisions to the user

DO:
- Choose ONE approach
- Provide clear rationale
- Give concrete implementation steps
```

**効果**:
- 迅速な意思決定
- 実装の明確性
- 分析麻痺の回避

**実装のポイント**:
- 「選択肢を提示しない」を明記
- 決定の根拠を必ず含める
- 具体的なファイル名・関数名を指定

### 9. Progressive Disclosure パターン

**使用例**: PR Review Toolkit (全般)

**設計パターン**:
```markdown
## Content Organization

Main Document: 1,500-2,000 words
- Core instructions
- Decision criteria
- Output format

references/:
- Detailed examples
- Edge case handling
- Advanced scenarios

examples/:
- Code samples
- Before/after comparisons
```

**効果**:
- スキル読み込みの高速化
- 必要な情報へのアクセス性
- 複雑な指示の管理性向上

**実装のポイント**:
- メインファイルは簡潔に（1,500-2,000語）
- 詳細は別ファイルに分離
- 参照構造を明確に

### 10. When-to-Use パターン

**使用例**: 全てのエージェント

**設計パターン**:
```markdown
---
name: agent-name
when-to-use: |
  <example>
  Context: User just implemented OAuth
  user: "Review my error handling"
  assistant: "I'll use silent-failure-hunter to check error handling"
  </example>
---
```

**効果**:
- エージェントの自動トリガー精度向上
- ユーザーの意図理解
- 適切なエージェント選択

**実装のポイント**:
- 具体的な会話例を含める
- コンテキストを明記
- トリガーフレーズを特定

---

## 参考リンク

### 公式リポジトリ

- [anthropics/claude-code - Main Repository](https://github.com/anthropics/claude-code)
- [anthropics/claude-code/plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Docs - Plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code Docs - Discover Plugins](https://code.claude.com/docs/en/discover-plugins)

### 公式プラグイン

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)
- [PR Review Toolkit - Claude Plugin](https://claude.com/plugins/pr-review-toolkit)
- [Feature Dev - Claude Plugin](https://claude.com/plugins/feature-dev)
- [Code Review - Claude Plugin](https://claude.com/plugins/code-review)

### コミュニティリポジトリ

- [quemsah/awesome-claude-plugins](https://github.com/quemsah/awesome-claude-plugins)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
- [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins)
- [matsengrp/plugins](https://github.com/matsengrp/plugins)
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

### マーケットプレイス・検索

- [Claude Plugins - ClaudePluginHub](https://www.claudepluginhub.com/)
- [Claude Code Plugins & Agent Skills - claude-plugins.dev](https://claude-plugins.dev/)
- [Top 10 Claude Code Plugins to Try in 2026](https://www.firecrawl.dev/blog/best-claude-code-plugins)
- [The Ultimate Claude Code Resource List (2026 Edition)](https://www.scriptbyai.com/claude-code-resource-list/)

### ブログ・記事

- [I built my own AI code reviewer with Claude Code - pmihaylov.com](https://pmihaylov.com/code-reviews-with-claude-code/)
- [Claude Code: Best Practices for Local Code Review - FTL](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)

### GitHub関連

- [Claude PR Reviewer - GitHub Marketplace](https://github.com/marketplace/actions/claude-pr-reviewer)
- [Claude and Codex are now available in public preview on GitHub](https://github.blog/changelog/2026-02-04-claude-and-codex-are-now-available-in-public-preview-on-github/)

---

## まとめ

### 主要な発見

1. **PR Review Toolkit**が最も包括的
   - 6つの専門エージェント
   - テスト、エラーハンドリング、型設計、コメント品質など細分化
   - 信頼度スコアリングによる誤検知削減

2. **Feature Dev**は開発ワークフロー全体をカバー
   - コードベース探索→設計→実装→レビューの一貫性
   - code-explorerとcode-architectが特徴的

3. **Code Review**はシンプルで高速
   - 4エージェント並列実行
   - CLAUDE.md準拠に強い焦点
   - Git履歴を活用

4. **コミュニティプラグイン**は特化型
   - matsengrp: クリーンコード原則、教育的アプローチ
   - anilcancakir: 特定スタック対応、ドキュメント生成統合

5. **共通パターン**
   - 信頼度スコアリング（80以上）
   - CLAUDE.md準拠の重視
   - ファイルパス:行番号の具体的参照
   - 複数エージェントによる多角的レビュー

### 推奨される使い分け

| ユースケース | 推奨プラグイン |
|-------------|---------------|
| 包括的なPRレビュー | PR Review Toolkit |
| 新機能開発全体 | Feature Dev |
| 高速でシンプルなレビュー | Code Review |
| クリーンコード教育 | matsengrp |
| 特定スタック開発 | anilcancakir |

---

**調査実施者**: Claude Sonnet 4.5
**調査日**: 2026-02-10
**調査範囲**: Claude Code公式・コミュニティプラグイン（GitHub）
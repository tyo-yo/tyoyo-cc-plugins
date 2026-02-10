# コードレビュー観点リスト（2026年版）

調査日: 2026-02-10
調査元: Claude Code公式プラグイン、コミュニティプラグイン、業界ベストプラクティス

## 目次

1. [観点カテゴリ概要](#観点カテゴリ概要)
2. [詳細観点リスト](#詳細観点リスト)
3. [エージェント設計への推奨マッピング](#エージェント設計への推奨マッピング)

---

## 観点カテゴリ概要

コードレビュー観点を8つの主要カテゴリに分類：

| カテゴリ | 観点数 | 優先度 | 説明 |
|---------|-------|--------|------|
| **プロジェクト標準** | 3 | 高 | プロジェクト固有のルールと一貫性 |
| **正確性** | 5 | 最高 | バグ、セキュリティ、エッジケース |
| **品質と保守性** | 6 | 高 | 読みやすさ、複雑性、保守性 |
| **テストとエラー処理** | 4 | 最高 | テスト品質、エラーハンドリング |
| **設計とアーキテクチャ** | 5 | 中〜高 | 型設計、アーキテクチャパターン |
| **ドキュメント** | 2 | 中 | コメント品質、ドキュメント精度 |
| **パフォーマンスとアクセシビリティ** | 3 | 中 | パフォーマンス、アクセシビリティ |
| **コンテキスト分析** | 2 | 中 | Git履歴、コードベース理解 |

**合計30観点**

---

## 詳細観点リスト

### 1. プロジェクト標準（Project Standards）

#### 1.1 CLAUDE.md準拠（CLAUDE.md Compliance）

**目的**: プロジェクト固有のガイドラインへの準拠確認

**チェック内容**:
- インポートパターンの遵守
- フレームワーク規約の適用
- スタイルガイドラインの順守
- 命名規則の一貫性
- ロギング規約の適用
- エラーハンドリング規約の適用

**信頼度基準**:
- 91-100点: CLAUDE.mdに明示的に記載されたルールへの直接的な違反
- 80-90点: ガイドラインに暗黙的に含まれる重要な慣習からの逸脱

**出力フォーマット**:
```markdown
**Issue**: [違反内容]
- **Guideline**: "CLAUDE.md says: [引用]"
- **Location**: [ファイルパス:行番号]
- **Fix**: [修正提案]
- **Confidence**: [スコア]
```

**既存プラグイン**: PR Review Toolkit (code-reviewer), Feature Dev (code-reviewer), Code Review (2エージェント)

---

#### 1.2 コーディング規約の一貫性（Coding Convention Consistency）

**目的**: コードベース全体での一貫性確保

**チェック内容**:
- 命名規則の統一（camelCase、snake_case、PascalCase）
- インデントとフォーマットの一貫性
- モジュール構造の統一
- ファイル配置パターンの統一
- コメントスタイルの統一

**信頼度基準**:
- 80-100点: 既存コードと明らかに矛盾するパターン
- 50-79点: 軽微な不一致

**既存プラグイン**: code-simplifier, matsengrp (clean-code-reviewer)

---

#### 1.3 既存パターンとの整合性（Existing Pattern Alignment）

**目的**: 既存コードベースのアーキテクチャパターンとの整合性確認

**チェック内容**:
- 類似機能の実装方法との一致
- ディレクトリ構造の慣習遵守
- 依存関係管理パターンの統一
- 状態管理パターンの統一
- API設計パターンの統一

**信頼度基準**:
- 85-100点: 既存の確立されたパターンからの明確な逸脱
- 70-84点: パターン選択の不整合

**既存プラグイン**: Feature Dev (code-architect, code-explorer)

---

### 2. 正確性（Correctness）

#### 2.1 バグ検出（Bug Detection）

**目的**: ロジックエラー、実行時エラー、機能不全の特定

**チェック内容**:
- ロジックエラー（条件式の誤り、演算子の誤用）
- Null/undefined参照
- 配列境界エラー
- 型エラー（型安全性の欠如）
- メモリリーク
- 競合状態
- 無限ループ
- Off-by-one エラー
- 初期化エラー

**信頼度基準**:
- 91-100点: 必ず発生する実行時エラーまたは重大なロジックエラー
- 80-90点: 特定条件下で発生する高確率のバグ

**出力フォーマット**:
```markdown
**Bug**: [説明]
- **Impact**: [影響範囲]
- **Location**: [ファイルパス:行番号]
- **Reproduction**: [再現手順]
- **Fix**: [修正提案]
- **Confidence**: [スコア]
```

**既存プラグイン**: すべての公式プラグイン（code-reviewer, Code Review）

---

#### 2.2 セキュリティ脆弱性（Security Vulnerabilities）

**目的**: セキュリティリスクの特定

**チェック内容**:
- 入力検証の欠如
- SQLインジェクション脆弱性
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- コマンドインジェクション
- パストラバーサル
- 認証・認可の不備
- 機密データの不適切な処理（ログ出力、平文保存）
- 安全でない依存関係の使用
- ハードコードされた認証情報

**信頼度基準**:
- 91-100点: 明確に悪用可能なセキュリティホール
- 80-90点: 潜在的なセキュリティリスク

**出力フォーマット**:
```markdown
**Vulnerability**: [脆弱性の種類]
- **Severity**: CRITICAL/HIGH/MEDIUM/LOW
- **Attack Vector**: [攻撃手法]
- **Location**: [ファイルパス:行番号]
- **Fix**: [修正提案]
- **Reference**: [CWE/OWASP参照]
- **Confidence**: [スコア]
```

**既存プラグイン**: PR Review Toolkit (code-reviewer), anilcancakir (my_review)

---

#### 2.3 エッジケースとバウンダリー条件（Edge Cases & Boundary Conditions）

**目的**: 極端な入力や境界条件での正しい動作確認

**チェック内容**:
- Null/undefined/空文字列の処理
- 空配列/空オブジェクトの処理
- 数値の境界値（0、負数、最大値、最小値）
- 文字列の境界値（空、最大長）
- タイムゾーン、日時の境界値
- ファイルサイズの制限
- 同時実行の制限
- ネットワークタイムアウト

**信頼度基準**:
- 85-100点: 明らかに未処理のエッジケース
- 70-84点: 潜在的な境界値問題

**既存プラグイン**: pr-test-analyzer（間接的）

**2026年トレンド**: AIコードは「ハッピーパス」に強いがエッジケースに弱い傾向

---

#### 2.4 サイレントフェイラー（Silent Failures）

**目的**: エラーが適切に伝播・通知されるか確認

**チェック内容**:
- 空のcatchブロック
- エラーをログのみで吸収
- 無言でデフォルト値を返す
- 不適切なフォールバック動作
- ユーザーへのフィードバック欠如
- 広すぎる例外捕捉（catch-all）
- 本番コードのモック実装
- 説明なしの再試行

**信頼度基準**:
- 91-100点: 致命的なエラーが完全に隠蔽される
- 80-90点: エラーが適切に伝播されない

**出力フォーマット**:
```markdown
**Silent Failure**: [問題説明]
- **Location**: [ファイルパス:行番号]
- **Severity**: CRITICAL/HIGH/MEDIUM
- **What could go wrong**: [潜在エラー]
- **User impact**: [ユーザー影響]
- **Recommendation**: [推奨対応]
- **Fix example**: [修正例コード]
- **Confidence**: [スコア]
```

**既存プラグイン**: PR Review Toolkit (silent-failure-hunter)

**2026年トレンド**: AI生成コードで特に多い問題パターン

---

#### 2.5 機能要件の適合性（Functional Requirements Compliance）

**目的**: 実装が要件を満たしているか確認

**チェック内容**:
- PRの説明に記載された機能の実現
- ビジネスロジックの正確性
- ユーザーストーリーの達成
- 期待される入出力の一致
- 仕様書との整合性

**信頼度基準**:
- 91-100点: 明らかな機能不足または誤実装
- 80-90点: 部分的な要件未達

**既存プラグイン**: なし（新規観点）

---

### 3. 品質と保守性（Quality & Maintainability）

#### 3.1 読みやすさ（Readability）

**目的**: コードの理解しやすさ評価

**チェック内容**:
- 明確で説明的な変数名
- 適切な関数分割
- 深すぎるネスト（3階層以上）
- 複雑な三項演算子の連鎖
- マジックナンバー
- 長すぎる関数（50行以上）
- 長すぎる行（120文字以上）

**信頼度基準**:
- 80-100点: 明らかに理解困難なコード

**既存プラグイン**: code-simplifier, matsengrp (clean-code-reviewer)

---

#### 3.2 複雑性（Complexity）

**目的**: 循環的複雑度や認知的複雑度の評価

**チェック内容**:
- 高い循環的複雑度（McCabe > 10）
- 多数の分岐条件
- 深いネストレベル
- 長い関数やメソッド
- 複雑な条件式

**信頼度基準**:
- 85-100点: 保守が困難なレベルの複雑性

**既存プラグイン**: code-simplifier

---

#### 3.3 コード臭（Code Smells）

**目的**: リファクタリングが必要なコードパターンの検出

**チェック内容**:
- 重複コード
- 長いメソッド
- 大きなクラス
- 長いパラメータリスト
- 特性の横恋慕（Feature Envy）
- データの群れ（Data Clumps）
- プリミティブへの執着
- Switch文の乱用
- 一時フィールド
- メッセージチェーン

**信頼度基準**:
- 80-100点: 明確なコード臭のパターン

**出力フォーマット（教育的）**:
```markdown
**Code Smell**: [臭いの種類]
- **What**: [問題の説明]
- **Why it matters**: [なぜ問題か]
- **Location**: [ファイルパス:行番号]
- **How to fix**: [修正方法]
- **Learn more**: [参考資料]
- **Confidence**: [スコア]
```

**既存プラグイン**: matsengrp (code-smell-detector)

---

#### 3.4 アンチパターン（Anti-patterns）

**目的**: 設計上の悪いパターンの検出

**チェック内容**:
- God Object（神オブジェクト）
- Spaghetti Code（スパゲッティコード）
- Lava Flow（溶岩流）- 使われないコード
- Golden Hammer（黄金のハンマー）- 過度な技術依存
- Cargo Cult Programming（カーゴカルト）
- Premature Optimization（早すぎる最適化）
- Shotgun Surgery（ショットガン手術）
- Divergent Change（発散的変更）

**信頼度基準**:
- 85-100点: 明確なアンチパターン

**既存プラグイン**: matsengrp (antipattern-scanner)

---

#### 3.5 保守性（Maintainability）

**目的**: 将来の変更の容易さ評価

**チェック内容**:
- ハードコードされた値（設定ファイル化推奨）
- 古い依存関係
- 不要な複雑性
- モジュール性の欠如
- 密結合
- 低凝集度
- テスト性の低さ

**信頼度基準**:
- 80-100点: 保守性を著しく低下させる要因

**既存プラグイン**: code-simplifier

---

#### 3.6 クリーンコード原則（Clean Code Principles）

**目的**: Robert Martin氏のクリーンコード原則への準拠

**チェック内容**:
- SOLID原則の遵守
  - 単一責任の原則（SRP）
  - 開放閉鎖の原則（OCP）
  - リスコフの置換原則（LSP）
  - インターフェース分離の原則（ISP）
  - 依存関係逆転の原則（DIP）
- DRY原則（Don't Repeat Yourself）
- YAGNI（You Aren't Gonna Need It）
- KISS（Keep It Simple, Stupid）

**信頼度基準**:
- 85-100点: 原則への明確な違反

**既存プラグイン**: matsengrp (clean-code-reviewer)

---

### 4. テストとエラー処理（Testing & Error Handling）

#### 4.1 テストカバレッジ（Test Coverage）

**目的**: 振る舞いベースのテスト品質評価（行カバレッジではなく）

**チェック内容**:
- エラーハンドリングパスのテスト
- 境界値とエッジケースのテスト
- ビジネスロジック分岐のカバー
- 負のテストケース（失敗パス）
- 統合テストの適切性
- テストの振る舞い焦点（実装詳細ではなく）

**重大度評価**:
- 9-10点: データ喪失やセキュリティにつながる重大機能
- 5-8点: ユーザー影響のある重要ロジック
- 1-4点: 補完的カバレッジ

**出力フォーマット**:
```markdown
**Test Gap**: [未カバー項目]
- **Severity**: [1-10]
- **Location**: [ファイルパス:行番号]
- **Risk**: [リスク説明]
- **Missing test**: [必要なテストケース]
- **Suggested test**: [テストコード例]
- **Confidence**: [スコア]
```

**既存プラグイン**: PR Review Toolkit (pr-test-analyzer), matsengrp (pre-pr-check)

---

#### 4.2 エラーハンドリング品質（Error Handling Quality）

**目的**: エラー処理の適切性評価

**チェック内容**:
- 適切なログレベルの使用
- 充分なコンテキスト情報
- エラーIDの付与
- ユーザーへの明確なフィードバック
- 実行可能な対応策の提示
- 技術詳細の適切な露出
- キャッチの特異性（広すぎないか）
- エラー伝播の適切性

**信頼度基準**:
- 91-100点: 致命的なエラーハンドリングの欠陥
- 80-90点: 不適切なエラー処理

**既存プラグイン**: PR Review Toolkit (silent-failure-hunter)

---

#### 4.3 テストの質（Test Quality）

**目的**: テストコード自体の品質評価

**チェック内容**:
- リファクタリング後も有効か（実装詳細に依存していないか）
- テストの独立性
- テストの決定性（非決定的テストの排除）
- テストの明確性（AAA: Arrange-Act-Assert）
- 適切なアサーション
- テストの保守性

**信頼度基準**:
- 80-100点: 明らかに脆弱なテスト設計

**既存プラグイン**: PR Review Toolkit (pr-test-analyzer)

---

#### 4.4 例外安全性（Exception Safety）

**目的**: 例外発生時の安全性確認

**チェック内容**:
- リソースリークの回避（finally/defer/RAII）
- トランザクションの整合性
- 状態の一貫性維持
- 例外中立性
- 適切な例外型の選択

**信頼度基準**:
- 85-100点: 例外安全性の明確な欠如

**既存プラグイン**: なし（新規観点）

---

### 5. 設計とアーキテクチャ（Design & Architecture）

#### 5.1 型設計とカプセル化（Type Design & Encapsulation）

**目的**: 型の不変性（invariants）とカプセル化の評価

**チェック内容**:
- 不変性の識別と表現
- カプセル化評価（1-10）
  - 内部実装の隠蔽
  - 外部からの違反可能性
  - アクセス修飾子の適切性
- 不変性表現評価（1-10）
  - 構造による明確性
  - コンパイル時強制可能性
  - 自己説明性
- 不変性有用性評価（1-10）
  - 実バグ防止性
  - ビジネス要件適合性
  - 推論容易性

**信頼度基準**:
- 85-100点: 型設計の明確な欠陥

**出力フォーマット**:
```markdown
**Type**: [型名]
- **Identified Invariants**: [不変性リスト]
- **Ratings**:
  - Encapsulation: [1-10] - [根拠]
  - Invariant Expression: [1-10] - [根拠]
  - Invariant Usefulness: [1-10] - [根拠]
- **Strengths**: [強み]
- **Concerns**: [懸念事項]
- **Improvements**: [改善提案]
- **Confidence**: [スコア]
```

**既存プラグイン**: PR Review Toolkit (type-design-analyzer)

**適用言語**: TypeScript、Java、C#、Rust、Go等の型安全言語

---

#### 5.2 アーキテクチャパターン準拠（Architecture Pattern Compliance）

**目的**: 既存アーキテクチャパターンへの適合性確認

**チェック内容**:
- レイヤー構造の遵守（プレゼンテーション→ビジネスロジック→データ）
- デザインパターンの適切な使用
- コンポーネント間のインターフェース
- 横断的関心事の分離（認証、ログ、キャッシング）
- 依存関係の方向性

**信頼度基準**:
- 85-100点: アーキテクチャ原則からの明確な逸脱

**既存プラグイン**: Feature Dev (code-architect), matsengrp (antipattern-scanner)

---

#### 5.3 API設計（API Design）

**目的**: APIの使いやすさと一貫性評価

**チェック内容**:
- RESTful原則の遵守（該当する場合）
- 一貫したエンドポイント命名
- 適切なHTTPメソッドの使用
- エラーレスポンスの標準化
- バージョニング戦略
- ドキュメントとの整合性
- 後方互換性の考慮

**信頼度基準**:
- 80-100点: API設計の重大な問題

**既存プラグイン**: なし（新規観点）

---

#### 5.4 依存関係管理（Dependency Management）

**目的**: 依存関係の適切性評価

**チェック内容**:
- 循環依存の回避
- 適切な抽象化レベル
- 依存関係の最小化
- 外部ライブラリの適切な選択
- バージョン固定の適切性
- セキュリティ脆弱性のある依存関係

**信頼度基準**:
- 85-100点: 依存関係の重大な問題

**既存プラグイン**: Feature Dev (code-explorer)

---

#### 5.5 データフロー設計（Data Flow Design）

**目的**: データの流れと変換の明確性評価

**チェック内容**:
- データ変換の明確性
- 状態変化の追跡可能性
- 副作用の明示性
- データの不変性
- ストリーム処理の適切性

**信頼度基準**:
- 80-100点: データフローの混乱

**既存プラグイン**: Feature Dev (code-explorer, code-architect)

---

### 6. ドキュメント（Documentation）

#### 6.1 コメント品質と精度（Comment Quality & Accuracy）

**目的**: コード内コメントの精度と有用性評価

**チェック内容**:
- 事実検証（署名、戻り値、型参照が実装と一致）
- 完全性評価（前提条件、副作用、エラー処理の説明）
- 長期価値評価（「なぜ」の説明を重視、自明なコメントは削除対象）
- 誤解要因の特定（曖昧性、古い参照、矛盾）
- 改善提案（具体的で実行可能なフィードバック）

**信頼度基準**:
- 91-100点: 実装と矛盾する不正確なコメント
- 80-90点: 誤解を招くまたは陳腐化したコメント

**出力フォーマット**:
```markdown
## Comment Analysis

### Critical Issues
[不正確または誤解招く箇所]

### Improvement Opportunities
[強化可能な部分]

### Candidates for Removal
[不要なコメント（自明な繰り返し）]

### Good Examples
[参考になるコメント例]
```

**既存プラグイン**: PR Review Toolkit (comment-analyzer)

---

#### 6.2 ドキュメント整合性（Documentation Consistency）

**目的**: コードとドキュメントの整合性確認

**チェック内容**:
- README、仕様書との一致
- APIドキュメントの正確性
- インラインドキュメント（JSDoc、PHPDoc等）の更新
- 変更履歴の記録
- 設定ファイルのコメント

**信頼度基準**:
- 85-100点: ドキュメントと実装の明確な不一致

**既存プラグイン**: anilcancakir (my_docs)

---

### 7. パフォーマンスとアクセシビリティ（Performance & Accessibility）

#### 7.1 パフォーマンス（Performance）

**目的**: 明らかな非効率性の検出

**チェック内容**:
- 無限ループや終了しないループ
- N+1クエリ問題
- 過剰なメモリ割り当て
- 不要なネットワークリクエスト
- 高コストな操作の繰り返し
- キャッシング機会の欠如
- データベースインデックスの欠如

**重要**: パフォーマンスクリティカルなパスのみを対象。理論的な最適化は避ける。

**信頼度基準**:
- 85-100点: 明らかなパフォーマンスボトルネック
- 70-84点: 潜在的なパフォーマンス問題

**既存プラグイン**: なし（一般的なcode-reviewerが部分的にカバー）

**2026年トレンド**: 実際のリスク対象、理論的な速度ではない

---

#### 7.2 アクセシビリティ（Accessibility）

**目的**: WCAG準拠とアクセシビリティ標準の確認

**チェック内容**:
- セマンティックHTMLの使用
- ARIA属性の適切な使用
- キーボードナビゲーション対応
- スクリーンリーダー対応
- 色コントラスト
- フォーカス管理
- ネイティブHTML要素の活用（button、dialog等）

**信頼度基準**:
- 85-100点: WCAG違反

**既存プラグイン**: なし（新規観点）

**2026年トレンド**: ネイティブパターンの活用推奨

---

#### 7.3 リソース管理（Resource Management）

**目的**: リソースの適切な管理確認

**チェック内容**:
- ファイルハンドルのクローズ
- データベース接続のクローズ
- メモリリークの回避
- タイマーのクリーンアップ
- イベントリスナーの解除

**信頼度基準**:
- 91-100点: 確実なリソースリーク
- 80-90点: 潜在的なリソースリーク

**既存プラグイン**: 一般的なcode-reviewerが部分的にカバー

---

### 8. コンテキスト分析（Context Analysis）

#### 8.1 Git履歴分析（Git History Analysis）

**目的**: 過去の変更履歴から問題パターンを検出

**チェック内容**:
- 同じ箇所での繰り返されるバグ修正
- リファクタリング後の不整合
- 過去に削除されたが復活した問題コード
- コミットメッセージとの整合性
- 変更頻度の高いファイル（ホットスポット）

**信頼度基準**:
- 80-100点: 過去のパターンから明確に予測される問題

**既存プラグイン**: Code Review (履歴分析エージェント)

---

#### 8.2 コードベース理解（Codebase Understanding）

**目的**: 既存コードベースの深い理解に基づくレビュー

**チェック内容**:
- エントリーポイントから出力までの実行フロー
- データ変換の追跡
- 依存関係と統合の理解
- 状態変化と副作用の文書化
- アーキテクチャレイヤーの理解

**信頼度基準**:
- 85-100点: コードベースの理解不足による問題

**既存プラグイン**: Feature Dev (code-explorer)

---

## エージェント設計への推奨マッピング

### 基本方針

1. **1エージェント = 1〜3観点**: 専門性を保つ
2. **並列実行可能**: 観点間の依存関係を最小化
3. **信頼度スコアリング**: すべてのエージェントで80+基準を採用
4. **カスタマイズ可能**: 観点の追加・削除が容易

---

### 推奨エージェント構成（15エージェント）

#### Tier 1: 必須エージェント（高優先度）

| エージェント名 | 観点 | モデル | 理由 |
|--------------|------|--------|------|
| **guideline-enforcer** | CLAUDE.md準拠、コーディング規約の一貫性 | Sonnet | プロジェクト標準の最重要チェック |
| **bug-hunter** | バグ検出、機能要件の適合性 | Opus | 最も重要な正確性チェック |
| **security-guardian** | セキュリティ脆弱性 | Opus | セキュリティは最高優先度 |
| **silent-failure-detector** | サイレントフェイラー、エラーハンドリング品質 | Sonnet | AIコードの典型的問題 |
| **test-quality-checker** | テストカバレッジ、テストの質 | Sonnet | 品質保証の基盤 |

#### Tier 2: 推奨エージェント（高〜中優先度）

| エージェント名 | 観点 | モデル | 理由 |
|--------------|------|--------|------|
| **edge-case-validator** | エッジケースとバウンダリー条件 | Sonnet | AIコードの弱点 |
| **readability-enhancer** | 読みやすさ、複雑性、コード臭 | Haiku | 保守性の基盤 |
| **architecture-analyst** | アーキテクチャパターン準拠、既存パターンとの整合性 | Sonnet | 設計の一貫性 |
| **type-design-reviewer** | 型設計とカプセル化 | Sonnet | 型安全言語での重要性 |
| **comment-accuracy-checker** | コメント品質と精度 | Haiku | ドキュメント品質 |

#### Tier 3: オプションエージェント（中〜低優先度）

| エージェント名 | 観点 | モデル | 理由 |
|--------------|------|--------|------|
| **clean-code-mentor** | クリーンコード原則、アンチパターン | Haiku | 教育的価値 |
| **performance-auditor** | パフォーマンス、リソース管理 | Haiku | クリティカルパスのみ |
| **accessibility-checker** | アクセシビリティ | Haiku | UI/Web開発向け |
| **git-history-analyzer** | Git履歴分析 | Haiku | コンテキスト理解 |
| **api-design-reviewer** | API設計、ドキュメント整合性 | Haiku | API開発向け |

---

### エージェント並列実行戦略

#### 並列グループ1（コア品質）
- guideline-enforcer
- bug-hunter
- security-guardian
- silent-failure-detector

**実行時間**: 並列実行により最も遅いエージェントの時間（約2-3分）

#### 並列グループ2（補足品質）
- test-quality-checker
- edge-case-validator
- readability-enhancer
- architecture-analyst

**実行時間**: 約2-3分

#### 並列グループ3（詳細分析）
- type-design-reviewer
- comment-accuracy-checker
- その他のオプションエージェント

**実行時間**: 約1-2分

---

### カスタマイズ方法

#### 観点の追加

```yaml
# .claude/custom-code-review.local.md
---
enabled_perspectives:
  - guideline-enforcer
  - bug-hunter
  - security-guardian
  - silent-failure-detector
  - test-quality-checker
  - my-custom-perspective  # 追加

custom_perspectives:
  - name: my-custom-perspective
    description: "カスタム観点の説明"
    model: sonnet
    focus_areas:
      - "チェック項目1"
      - "チェック項目2"
    confidence_threshold: 80
---
```

#### 観点の無効化

```yaml
disabled_perspectives:
  - accessibility-checker  # UI開発以外では不要
  - performance-auditor    # パフォーマンスクリティカルでなければスキップ
```

---

## 参考資料

### 公式プラグイン
- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)

### ベストプラクティス（2026年）
- [Claude Code Best Practices for Local Code Review](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)
- [Edge Cases and Error Handling: Where AI Code Falls Short](https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/)
- [8 Best AI Code Review Tools That Catch Real Bugs in 2026](https://www.qodo.ai/blog/best-ai-code-review-tools-2026/)

### コミュニティプラグイン
- [matsengrp/plugins](https://github.com/matsengrp/plugins)
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)

---

**作成日**: 2026-02-10
**作成者**: Claude Sonnet 4.5

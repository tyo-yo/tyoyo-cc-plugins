# 最終確定：39観点リスト

作成日: 2026-02-10
バージョン: 3.0（最終確定版）

---

## 📊 変更サマリー

- **元**: 50観点
- **統合**: -2（1.1+1.2統合、6.6→6.7統合）
- **削除**: -9（TDD、保守性、技術的厳密性、メタ観点5つ）
- **最終**: **39観点**

---

## 🗂️ カテゴリ別観点数

| # | カテゴリ | 観点数 | 優先度 |
|---|---------|-------|--------|
| 1 | **プロジェクト標準** | 2 | 高 |
| 2 | **正確性（基本）** | 5 | 最高 |
| 3 | **セキュリティ（基本）** | 4 | 最高 |
| 4 | **セキュリティ（高度）** | 6 | 高 |
| 5 | **テストとエラー処理** | 5 | 最高 |
| 6 | **品質と保守性** | 4 | 高 |
| 7 | **設計とアーキテクチャ** | 6 | 中〜高 |
| 8 | **ドキュメント** | 2 | 中 |
| 9 | **パフォーマンス** | 3 | 中 |
| 10 | **コンテキスト分析** | 2 | 中〜高 |

**合計**: 39観点

---

## 📋 完全な39観点リスト

### 1. プロジェクト標準（2観点）

#### P01: AIエージェント向け指示の遵守（統合）
- **元観点**: 1.1 CLAUDE.md準拠 + 1.2 コーディング規約の一貫性
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点（明示的違反）、80-90点（暗黙的違反）
- **適用基準**:
  - ✅ 常に適用
  - すべてのコード変更
- **対象ドキュメント**:
  - CLAUDE.md（Claude Code）
  - .cursorrules（Cursor）
  - プロジェクト独自のコーディングガイドライン
  - README内のAI向けセクション
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev
  - https://github.com/matsengrp/plugins

#### P02: 既存パターンとの整合性
- **元ID**: P03-PATTERN_ALIGNMENT
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ 新機能追加
  - ✅ アーキテクチャ変更
  - ❌ 単純なバグ修正
  - ❌ ドキュメント変更のみ
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev

---

### 2. 正確性（基本）（5観点）

#### C01: バグ検出
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点（必ず発生）、80-90点（高確率）
- **適用基準**: ✅ 常に適用
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://github.com/anthropics/claude-code/tree/main/plugins/code-review
  - すべての公式プラグイン

#### C02: 機能要件の適合性
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点
- **適用基準**:
  - ✅ 新機能追加
  - ✅ 機能変更
  - ❌ リファクタリングのみ
- **ソース**: 新規観点（ベストプラクティスより）

#### C03: エッジケースとバウンダリー条件
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ ユーザー入力処理
  - ✅ データ変換処理
  - ✅ 境界値処理
- **2026年トレンド**: AIコードのハッピーパス偏重に対する対策
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/

#### C04: サイレントフェイラー
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点
- **適用基準**:
  - ✅ エラーハンドリング追加・変更
  - ✅ Try-catchブロックを含む
  - ✅ ログ処理変更
- **2026年トレンド**: AI生成コードで特に多い問題
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### C05: 例外安全性
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ リソース管理コード
  - ✅ トランザクション処理
  - ✅ ファイル/DB操作
- **ソース**: 新規観点（ベストプラクティスより）

---

### 3. セキュリティ（基本）（4観点）

#### S01: セキュリティ脆弱性（基本）
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点（明確）、80-90点（潜在的）
- **適用基準**: ✅ 常に適用
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://github.com/anilcancakir/claude-code-plugins

#### S02: 一般的な脆弱性パターン
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ セキュリティ関連コード
  - ✅ 認証・認可ロジック
  - ✅ 外部API呼び出し
- **ソース**: https://github.com/trailofbits/skills

#### S03: False Positiveフィルタリング
- **優先度**: Tier 1（必須）
- **信頼度基準**: 80以上のみ報告
- **適用基準**: ✅ セキュリティスキャン後の検証
- **ソース**: https://github.com/Piebald-AI/claude-code-system-prompts

#### S04: 先例ベースの評価
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**: ✅ 既存の安全パターンが存在する場合
- **ソース**: https://github.com/Piebald-AI/claude-code-system-prompts

---

### 4. セキュリティ（高度）（6観点）

#### S05: アダプティブレビュー深度 ⭐⭐⭐⭐⭐
- **優先度**: Tier 2（推奨）
- **信頼度基準**: コードベースサイズに応じた適応
- **適用基準**: ✅ セキュリティレビュー時
- **戦略**:
  - SMALL (<20ファイル): DEEP
  - MEDIUM (20-200): FOCUSED
  - LARGE (200+): SURGICAL
- **ソース**: https://github.com/trailofbits/skills

#### S06: 攻撃者モデリング ⭐⭐⭐⭐⭐
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点（HIGH RISKのみ）
- **適用基準**: ✅ HIGH RISKのセキュリティ問題のみ
- **ソース**: https://github.com/trailofbits/skills

#### S07: セキュリティリグレッション ⭐⭐⭐⭐⭐
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 91-100点
- **適用基準**:
  - ✅ セキュリティ関連コード変更
  - ✅ 過去にCVE修正があるファイル
- **ソース**: https://github.com/trailofbits/skills

#### S08: ブラストラジアス（影響範囲）分析 ⭐⭐⭐⭐
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ 共通関数・ユーティリティ変更
  - ✅ MEDIUM以上のリスク
- **ソース**: https://github.com/trailofbits/skills

#### S09: ベースラインコンテキスト構築
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 前処理（スコアリングなし）
- **適用基準**:
  - ✅ 初回レビュー時
  - ✅ 大規模セキュリティレビュー
- **ソース**: https://github.com/trailofbits/skills

#### S10: レッドフラグエスカレーション ⭐⭐⭐⭐⭐
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 100点（即座エスカレーション）
- **適用基準**:
  - ✅ セキュリティコミットからのコード削除
  - ✅ アクセス制御修飾子の削除
  - ✅ 検証削除（置換なし）
- **ソース**: https://github.com/trailofbits/skills

---

### 5. テストとエラー処理（5観点）

#### T01: テストカバレッジ
- **優先度**: Tier 1（必須）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ 新規機能追加
  - ✅ ロジック変更
  - ❌ ドキュメント変更のみ
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://github.com/matsengrp/plugins

#### T02: テストの質
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**: ✅ テストコード変更
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### T03: エラーハンドリング品質
- **優先度**: Tier 1（必須）
- **信頼度基準**: 91-100点
- **適用基準**: ✅ エラーハンドリング追加・変更
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### T04: リグレッションテスト
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ バグ修正PR
  - ✅ 過去にバグがあった箇所
- **ソース**: https://github.com/levnikolaevich/claude-code-skills

#### T05: E2Eテスト計画
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ ユーザーフロー変更
  - ✅ 統合機能追加
- **ソース**: https://github.com/levnikolaevich/claude-code-skills

---

### 6. 品質と保守性（4観点）

#### Q01: 読みやすさ
- **優先度**: Tier 1（必須）
- **信頼度基準**: 80-100点
- **適用基準**: ✅ 常に適用
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit
  - https://github.com/matsengrp/plugins

#### Q02: 複雑性
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ 複雑なロジック
  - ✅ 長い関数（50行以上）
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### Q03: コード臭
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ 新規実装
  - ✅ リファクタリング候補
- **ソース**: https://github.com/matsengrp/plugins

#### Q04: アンチパターン
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ アーキテクチャ変更
  - ✅ 大規模実装
- **対象**: 汎用的なアンチパターンのみ（言語非依存）
- **ソース**: https://github.com/matsengrp/plugins

#### Q05: YAGNIチェック（拡張版） ⭐⭐⭐⭐
- **元観点**: Q07 + Q06の一部（DRY、KISS）
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ 新規機能追加
  - ✅ 拡張性実装
  - ❌ 明確な要件に基づく実装
- **チェック内容**:
  - YAGNIチェック（grepで実際の使用確認）
  - ハードコード値の検出
  - DRY原則（重複コード）
  - KISS原則（過剰な複雑性）
- **ソース**: https://github.com/obra/superpowers

---

### 7. 設計とアーキテクチャ（6観点）

#### D01: 型設計とカプセル化
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ 新しい型・クラス追加
  - ✅ 型安全言語（TypeScript、Java、C#、Rust、Go）
- **対象**: Pydanticデータクラス含む
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### D02: アーキテクチャパターン準拠
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ アーキテクチャ変更
  - ✅ 新規コンポーネント追加
- **対象**: 3層アーキテクチャ、デザインパターン（GOF等）
- **ソース**:
  - https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev
  - https://github.com/matsengrp/plugins

#### D03: API設計
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 80-100点
- **適用基準**: ✅ API追加・変更
- **対象**: REST API、GraphQL API、Python SDK、TypeScript Library
- **ソース**: 新規観点（ベストプラクティスより）

#### D04: 依存関係管理
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ 依存関係追加・変更
  - ✅ ライブラリアップグレード
- **チェック内容**:
  - 循環依存（ツールで検出不可）
  - 依存関係の最小化
  - 適切な抽象化レベル
- **除外**: セキュリティ脆弱性（Dependabotで対応）
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev

#### D05: データフロー設計
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ データ変換ロジック
  - ✅ 状態管理変更
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev

#### D06: 修正の検証（Fix Review）
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 80-100点
- **適用基準**: ✅ バグ修正PR
- **ソース**: https://github.com/trailofbits/skills

---

### 8. ドキュメント（2観点）

#### DOC01: コメント品質と精度
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 91-100点（不正確）、80-90点（誤解招く）
- **適用基準**: ✅ コメント追加・変更
- **チェック内容**:
  - コメントの正確性
  - 過剰なコメント（AIの無駄なコメント）
  - コメント不足（複雑なロジック）
  - 自明なコメント（削除対象）
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

#### DOC02: ドキュメント整合性
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ APIドキュメント変更
  - ✅ README更新
- **チェック内容**:
  - ドキュメント未更新の検出
  - コードとドキュメントの不一致
- **ソース**: https://github.com/anilcancakir/claude-code-plugins

---

### 9. パフォーマンス（3観点）

#### PERF01: パフォーマンス
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 85-100点（明らか）、70-84点（潜在的）
- **適用基準**:
  - ✅ パフォーマンスクリティカルなパス
  - ✅ ループ、データベースクエリ
- **2026年トレンド**: 実際のリスク対象、理論的最適化は避ける
- **ソース**: 一般的なcode-reviewer

#### PERF02: アクセシビリティ
- **優先度**: Tier 3（オプション）
- **信頼度基準**: 85-100点
- **適用基準**: ✅ UI/Web開発のみ
- **2026年トレンド**: ネイティブHTML要素の活用推奨
- **ソース**: 新規観点（WCAG準拠）

#### PERF03: リソース管理
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 91-100点（確実）、80-90点（潜在的）
- **適用基準**:
  - ✅ ファイル/DB操作
  - ✅ タイマー、イベントリスナー
- **ソース**: 一般的なcode-reviewer

---

### 10. コンテキスト分析（2観点）

#### CTX01: Git履歴分析
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 80-100点
- **適用基準**:
  - ✅ 変更頻度の高いファイル
  - ✅ 過去にバグが多い箇所
- **チェック内容**:
  - バグの温床検出
  - リファクタリング後の不整合
  - 削除されたコードの復活
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/code-review

#### CTX02: コードベース理解
- **優先度**: Tier 2（推奨）
- **信頼度基準**: 85-100点
- **適用基準**:
  - ✅ 既存機能変更
  - ✅ 統合コード
- **チェック内容**:
  - エントリーポイントから出力までの実行フロー
  - 依存関係と統合の理解
  - アーキテクチャレイヤーの理解
- **ソース**: https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev

---

## 🗑️ 削除された観点（参考）

以下の観点は最終リストから削除されました：

1. **T04 TDD原則の遵守** - TDDプロジェクト固有フロー
2. **Q05 保守性** - 冗長（他観点に統合）
3. **Q06 クリーンコード原則** - Q05 YAGNIチェックに統合
4. **Q08 技術的厳密性** - レビュー受信側の観点（本プラグイン対象外）
5. **CTX03 プランとの整合性** - メタ観点（ワークフロー）
6. **CTX04 レビュータイミング遵守** - メタ観点（ワークフロー）
7. **CTX05 サブタスク並列化** - メタ観点（実行制御）
8. **CTX06 エージェントレビュー** - メタ観点（実行制御）
9. **CTX07 品質ゲートとスコアリング** - メタ観点（実行制御）

---

## 📚 ソース一覧

### 公式プラグイン
- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)

### コミュニティリポジトリ
- [obra/superpowers](https://github.com/obra/superpowers) - 48,935 ⭐
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - 4,310 ⭐
- [trailofbits/skills](https://github.com/trailofbits/skills) - 2,498 ⭐
- [nizos/tdd-guard](https://github.com/nizos/tdd-guard) - 1,747 ⭐
- [Gentleman-Programming/gentleman-guardian-angel](https://github.com/Gentleman-Programming/gentleman-guardian-angel) - 560 ⭐
- [bartolli/claude-code-typescript-hooks](https://github.com/bartolli/claude-code-typescript-hooks) - 167 ⭐
- [Veraticus/cc-tools](https://github.com/Veraticus/cc-tools) - 46 ⭐
- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [matsengrp/plugins](https://github.com/matsengrp/plugins)
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)

### ベストプラクティス記事
- [Claude Code Best Practices for Local Code Review](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)
- [Edge Cases and Error Handling: Where AI Code Falls Short](https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/)
- [8 Best AI Code Review Tools That Catch Real Bugs in 2026](https://www.qodo.ai/blog/best-ai-code-review-tools-2026/)

---

**作成日**: 2026-02-10
**バージョン**: 3.0
**総観点数**: 39
**次のステップ**: 各観点のマークダウンファイル作成

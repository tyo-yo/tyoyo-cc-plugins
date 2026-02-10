# コードレビュー観点調査 - ファイルインデックス

調査日: 2026-02-10
調査者: Claude Sonnet 4.5

## 📁 ファイル構成

### 主要レポート

| ファイル | 説明 | 行数 | 重要度 |
|---------|------|------|--------|
| **comprehensive-perspectives-integration.md** | 50観点の統合レポート（14ソースから抽出） | 425行 | ⭐⭐⭐⭐⭐ |
| **review-perspectives.md** | 30観点の詳細リスト（初期版） | 892行 | ⭐⭐⭐⭐ |
| **custom-code-review-plugin-design.md** | プラグイン設計書 | 1,319行 | ⭐⭐⭐⭐⭐ |
| **claude-code-review-plugins.md** | 既存プラグイン調査（5つ） | 1,164行 | ⭐⭐⭐⭐ |
| **new-repositories-summary.md** | 新規7リポジトリの詳細分析 | - | ⭐⭐⭐⭐ |

### プロンプトファイル（12個）

すべて `prompts/` ディレクトリに保存：

1. `piebald-ai-review-pr.md` - シンプルなPRレビュー
2. `piebald-ai-security-review.md` - 包括的セキュリティレビュー（⭐⭐⭐⭐⭐）
3. `trailofbits-differential-review.md` - 適応的セキュリティレビュー（⭐⭐⭐⭐⭐）
4. `trailofbits-adversarial-analysis.md` - 攻撃者モデリング
5. `trailofbits-vulnerability-patterns.md` - 脆弱性パターン10種
6. `trailofbits-fix-review.md` - 修正検証手法
7. `obra-code-reviewer-agent.md` - コードレビューアエージェント
8. `obra-receiving-code-review.md` - レビュー受信ガイドライン
9. `bartolli-typescript-hooks.md` - TypeScript品質フック
10. `nizos-tdd-guard.md` - TDD強制ツール
11. `veraticus-cc-tools.md` - Go製ユーティリティ
12. `gentleman-guardian-angel.md` - Pre-commit AIレビューツール

---

## 🎯 次のセッションで使うべきファイル

### 最優先

1. **comprehensive-perspectives-integration.md**
   - 50観点すべてを含む統合レポート
   - 14ソースのURL付き
   - 実装優先度マトリクス
   - 推奨エージェント構成（20エージェント）

2. **custom-code-review-plugin-design.md**
   - プラグインのアーキテクチャ設計
   - ディレクトリ構造
   - 設定ファイル仕様
   - エージェント自動生成の仕組み

### 参考資料

3. **new-repositories-summary.md**
   - 新規7リポジトリの詳細分析
   - 各リポジトリのユニークな貢献

4. **prompts/** ディレクトリ
   - 実際のプロンプト例（12個）
   - 実装時の参考

---

## 📊 調査結果サマリー

### 調査したリポジトリ（14ソース）

#### スター数順トップ7

| # | リポジトリ | Stars | タイプ |
|---|-----------|-------|--------|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | 48,935 ⭐ | Skills + Agents |
| 2 | [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | 4,310 ⭐ | System Prompts |
| 3 | [trailofbits/skills](https://github.com/trailofbits/skills) | 2,498 ⭐ | Security Skills |
| 4 | [nizos/tdd-guard](https://github.com/nizos/tdd-guard) | 1,747 ⭐ | TDD Enforcement |
| 5 | [Gentleman-Programming/gentleman-guardian-angel](https://github.com/Gentleman-Programming/gentleman-guardian-angel) | 560 ⭐ | Pre-commit AI |
| 6 | [bartolli/claude-code-typescript-hooks](https://github.com/bartolli/claude-code-typescript-hooks) | 167 ⭐ | TypeScript Hooks |
| 7 | [Veraticus/cc-tools](https://github.com/Veraticus/cc-tools) | 46 ⭐ | Go Tools |

#### 公式プラグイン（3つ）

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit) - 6エージェント
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev) - 3エージェント
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review) - 4エージェント

#### コミュニティプラグイン（2つ）

- [matsengrp/plugins](https://github.com/matsengrp/plugins) - クリーンコード重視
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins) - Pre-Commit Flow

#### スキルコレクション（2つ）

- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) - Production-ready skills
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) - 300+ agent skills

---

## 🔑 重要な発見

### 最も革新的な10観点

1. ⭐⭐⭐⭐⭐ **アダプティブレビュー深度** (Trail of Bits)
   - コードベースサイズで戦略変更（SMALL/MEDIUM/LARGE）

2. ⭐⭐⭐⭐⭐ **攻撃者モデリング** (Trail of Bits)
   - WHO/WHAT/WHERE分析 + EASY/MEDIUM/HARD悪用可能性評価

3. ⭐⭐⭐⭐ **ブラストラジアス分析** (Trail of Bits)
   - 優先度 = リスク × 呼び出し元数

4. ⭐⭐⭐⭐⭐ **セキュリティリグレッション** (Trail of Bits)
   - Git履歴で過去の修正が再発していないか自動チェック

5. ⭐⭐⭐⭐ **False Positiveフィルタリング** (Piebald-AI)
   - 2段階検証 + 17+ハード除外ルール

6. ⭐⭐⭐⭐ **先例ベースの評価** (Piebald-AI)
   - 安全なパターンを学習（React, 環境変数等）

7. ⭐⭐⭐⭐ **YAGNIチェック** (obra)
   - 実装前にgrepで実際の使用を確認

8. ⭐⭐⭐⭐⭐ **レッドフラグエスカレーション** (Trail of Bits)
   - セキュリティコミットからのコード削除を即座に報告

9. ⭐⭐⭐⭐ **サブタスク並列化** (Piebald-AI)
   - 検出と検証を分離、並列実行で高速化

10. ⭐⭐⭐⭐ **技術的厳密性** (obra)
    - "Thank you"禁止、コードで示す文化

---

## 📝 次のセッションで必要なコマンド

### ファイルの確認

```bash
# すべてのファイルが存在するか確認
ls -lh custom-code-review/research/

# 主要レポートを読む
cat custom-code-review/research/comprehensive-perspectives-integration.md

# 設計書を読む
cat custom-code-review/research/custom-code-review-plugin-design.md

# プロンプトファイルを確認
ls custom-code-review/research/prompts/
```

### 実装開始

```bash
# プラグインディレクトリの確認
ls custom-code-review/

# plugin.json の作成
# （設計書の Phase 1 を参照）
```

---

## ✅ 永続性チェックリスト

- [x] 50観点すべてが `comprehensive-perspectives-integration.md` に記録
- [x] 14ソースすべてのGitHub URLが含まれている
- [x] 12個のプロンプトファイルが保存されている
- [x] 設計書（1,319行）が保存されている
- [x] 実装優先度マトリクスが含まれている
- [x] 推奨エージェント構成（20エージェント）が記録されている
- [x] すべてのファイルがプロジェクトディレクトリ（custom-code-review/research/）に保存されている

---

## 🚀 次のステップ

次のセッションでは以下を実行：

1. `comprehensive-perspectives-integration.md` を読んで50観点を確認
2. `custom-code-review-plugin-design.md` を読んで設計を理解
3. Phase 1（基盤実装）を開始：
   - plugin.json 作成
   - 設定ファイルテンプレート作成
   - Tier 1エージェントテンプレート作成（5つ）

---

**最終更新**: 2026-02-10 20:45

# 包括的コードレビュー観点統合（14ソースから抽出）

調査日: 2026-02-10
総調査ソース数: 14リポジトリ/プラグイン

## エグゼクティブサマリー

14のリポジトリ・プラグインを調査し、**50の統合観点**を抽出しました。

### 調査ソース一覧（スター数順）

| # | リポジトリ | Stars | タイプ |
|---|-----------|-------|--------|
| 1 | obra/superpowers | 48,935 ⭐ | Skills + Agents |
| 2 | Piebald-AI/claude-code-system-prompts | 4,310 ⭐ | System Prompts |
| 3 | trailofbits/skills | 2,498 ⭐ | Security Skills |
| 4 | nizos/tdd-guard | 1,747 ⭐ | TDD Enforcement |
| 5 | Gentleman-Programming/gentleman-guardian-angel | 560 ⭐ | Pre-commit AI |
| 6 | bartolli/claude-code-typescript-hooks | 167 ⭐ | TypeScript Hooks |
| 7 | Veraticus/cc-tools | 46 ⭐ | Go Tools |
| 8-10 | Anthropic公式プラグイン (PR Review Toolkit, Feature Dev, Code Review) | - | Official |
| 11-12 | matsengrp, anilcancakir | - | Community |
| 13-14 | levnikolaevich, VoltAgent (skill collections) | - | Collections |

---

## 50の統合観点リスト

### 既存30観点からの変更点

**追加された観点（20個）**:
1. アダプティブレビュー深度（Trail of Bits）
2. 攻撃者モデリング（Trail of Bits）
3. セキュリティリグレッション（Trail of Bits）
4. 一般的な脆弱性パターン（Trail of Bits）
5. 修正の検証（Fix Review）（Trail of Bits）
6. ブラストラジアス分析（Trail of Bits）
7. ベースラインコンテキスト構築（Trail of Bits）
8. レッドフラグエスカレーション（Trail of Bits）
9. プランとの整合性（obra）
10. レビュータイミング遵守（obra）
11. YAGNIチェック（obra）
12. 技術的厳密性（obra）
13. False Positiveフィルタリング（Piebald-AI）
14. 先例ベースの評価（Piebald-AI）
15. サブタスク並列化（Piebald-AI）
16. TDD原則の遵守（TDD Guard）
17. リグレッションテスト（levnikolaevich）
18. E2Eテスト計画（levnikolaevich）
19. エージェントレビュー（複数モデル）（levnikolaevich）
20. 品質ゲートとスコアリング（levnikolaevich）

---

## 最も革新的な10の観点

### 1. アダプティブレビュー深度 ⭐⭐⭐⭐⭐
**ソース**: trailofbits/skills (differential-review)

**コードベースサイズ別戦略**:

| サイズ | ファイル数 | 戦略 | アプローチ |
|--------|----------|------|-----------|
| SMALL | <20 | DEEP | 全依存関係、完全git blame |
| MEDIUM | 20-200 | FOCUSED | 1ホップ依存、優先ファイル |
| LARGE | 200+ | SURGICAL | クリティカルパスのみ |

これにより、小規模プロジェクトでは徹底的に、大規模プロジェクトでは効率的にレビュー可能。

---

### 2. 攻撃者モデリング ⭐⭐⭐⭐⭐
**ソース**: trailofbits/skills (differential-review)

**攻撃者モデル**:
- **WHO**: 攻撃者タイプ（外部、内部、管理者）
- **WHAT**: 攻撃目標（データ窃取、DOS、権限昇格）
- **WHERE**: 攻撃ベクトル（ネットワーク、API、UI）

**悪用可能性評価**:
- **EASY**: 誰でも簡単
- **MEDIUM**: ある程度の知識必要
- **HARD**: 高度な専門知識必要

従来の「脆弱性あり/なし」ではなく、具体的な攻撃シナリオと悪用難易度を評価。

---

### 3. ブラストラジアス（影響範囲）分析 ⭐⭐⭐⭐
**ソース**: trailofbits/skills (differential-review)

**呼び出し元カウント**:
```bash
git grep "function_name" | wc -l
```

**優先度マトリクス**:
```
Priority = Risk Level × Blast Radius

Example:
- HIGH risk × 50 callers = TOP PRIORITY
- MEDIUM risk × 5 callers = LOWER PRIORITY
```

これにより、最も影響の大きい変更を優先的にレビュー。

---

### 4. セキュリティリグレッション検出 ⭐⭐⭐⭐⭐
**ソース**: trailofbits/skills (differential-review)

**Git履歴ベースの検出**:
```bash
# セキュリティコミットからのコード削除を検出
git log --grep="security|CVE|fix" --all --oneline
git diff <security-commit> HEAD -- <file>
```

過去に修正した脆弱性が再発していないか自動チェック。

---

### 5. False Positive フィルタリング ⭐⭐⭐⭐
**ソース**: Piebald-AI (security-review)

**2段階検証**:
1. 初期検出（過検出を許容）
2. 並列検証（問題ごとに独立サブタスク）

**17+のハード除外ルール**:
- Reactフレームワークの安全機能
- 環境変数（信頼された入力）
- ORMのパラメータ化クエリ
- フレームワーク提供のサニタイザー

信頼度≥8/10のみ報告 → ノイズ大幅削減。

---

### 6. 先例ベースの評価 ⭐⭐⭐⭐
**ソース**: Piebald-AI (security-review)

**信頼されたパターン**:
```typescript
const TRUSTED_PATTERNS = {
  xss: ['React.createElement', 'Angular sanitizer'],
  injection: ['parameterized queries', 'prepared statements'],
  secrets: ['process.env.*', 'vault API']
};
```

既知の安全なパターンを学習し、誤検知を削減。

---

### 7. YAGNI チェック ⭐⭐⭐⭐
**ソース**: obra/superpowers (receiving-code-review)

**実装前に使用確認**:
```bash
# 機能が実際に使われているか確認
grep -r "function_name" codebase/

# 使用されていない場合 → 削除提案（YAGNI）
```

過剰実装を防ぎ、コードベースをシンプルに保つ。

---

### 8. レッドフラグの即座エスカレーション ⭐⭐⭐⭐⭐
**ソース**: trailofbits/skills (differential-review)

**即座エスカレーション条件**:
- セキュリティコミット（"security", "CVE"）からのコード削除
- アクセス制御修飾子の削除
- 検証の削除（置換なし）
- 外部呼び出しの追加（チェックなし）
- 高ブラストラジアス（50+）+ HIGH リスク

これらを検出した瞬間、他のチェックをスキップして即座に報告。

---

### 9. サブタスク並列化 ⭐⭐⭐⭐
**ソース**: Piebald-AI (security-review)

**効率的な検証**:
```typescript
// Phase 1: Detection (1 subtask)
const allFindings = await detectVulnerabilities(code);

// Phase 2: Parallel Validation (N subtasks)
const validated = await Promise.all(
  allFindings.map(f => validateFinding(f))
);
```

検出と検証を分離し、検証を並列化することで高速化。

---

### 10. 技術的厳密性（No Performative Agreement） ⭐⭐⭐⭐
**ソース**: obra/superpowers (receiving-code-review)

**禁止される応答**:
- "You're absolutely right!"
- "Great point!"
- "Thanks for catching that!"

**推奨される応答**:
- "Fixed. [Brief description]"
- "Good catch - [specific issue]. Fixed in [location]."
- [Just fix and show in code]

レビューフィードバックを盲目的に受け入れず、コードベースと照合して検証。
間違っていれば技術的根拠をもって反論。

---

## 実装優先度マトリクス

### Tier 1: 絶対必須（10観点）

| 観点 | 理由 | ソース数 |
|------|------|---------|
| CLAUDE.md準拠 | プロジェクト標準の基盤 | 7 |
| バグ検出（一般） | 最も基本的な品質保証 | 14 |
| セキュリティ脆弱性（基本） | セキュリティは最優先 | 8 |
| サイレントフェイラー | 2026年AIコードの典型的問題 | 2 |
| テストカバレッジ | 品質保証の基盤 | 5 |
| 読みやすさ | 保守性の基盤 | 4 |
| コーディング規約 | 一貫性の基盤 | 14 |
| アーキテクチャパターン | 設計品質の基盤 | 4 |
| Git履歴分析（基本） | コンテキスト理解 | 3 |
| False Positiveフィルタリング | ノイズ削減 | 2 |

### Tier 2: 強く推奨（15観点）

- セキュリティ脆弱性（高度）+ 攻撃者モデリング
- セキュリティリグレッション
- エッジケース（AIコードの弱点）
- エラーハンドリング品質
- 既存パターンとの整合性
- コード臭
- テストの質
- 型設計
- コメント品質
- アダプティブレビュー深度
- ブラストラジアス分析
- YAGNI チェック
- TDD原則
- スマートキャッシング
- レッドフラグエスカレーション

### Tier 3: オプション（25観点）

残りの観点は、プロジェクトやチームのニーズに応じて選択。

---

## 推奨エージェント構成（20エージェント）

### Tier 1: 必須（7エージェント）

1. **guideline-enforcer** - CLAUDE.md準拠、コーディング規約
2. **bug-hunter** - バグ検出、機能要件適合
3. **security-guardian-basic** - セキュリティ脆弱性（基本）
4. **silent-failure-detector** - サイレントフェイラー、エラーハンドリング
5. **test-coverage-checker** - テストカバレッジ、テストの質
6. **readability-enhancer** - 読みやすさ、複雑性
7. **false-positive-filter** - 偽陽性フィルタリング

### Tier 2: 推奨（8エージェント）

8. **security-guardian-advanced** - セキュリティ脆弱性（高度）+ 攻撃者モデリング
9. **security-regression-hunter** - セキュリティリグレッション
10. **edge-case-validator** - エッジケース、バウンダリー条件
11. **architecture-analyst** - アーキテクチャパターン、既存パターン整合性
12. **code-smell-detector** - コード臭、アンチパターン
13. **type-design-reviewer** - 型設計、カプセル化
14. **comment-accuracy-checker** - コメント品質、精度
15. **git-history-analyzer** - Git履歴分析（基本 + 高度）

### Tier 3: オプション（5エージェント）

16. **tdd-enforcer** - TDD原則の遵守
17. **performance-auditor** - パフォーマンス、リソース管理
18. **accessibility-checker** - アクセシビリティ（UI/Web開発向け）
19. **api-design-reviewer** - API設計、ドキュメント整合性
20. **fix-reviewer** - 修正の検証

---

## Trail of Bits方式の6フェーズワークフロー

最も包括的なレビューワークフロー：

### Pre-Analysis: ベースラインコンテキスト構築
- システム全体の不変条件
- 信頼境界
- 検証パターン
- コールグラフ
- 状態フロー

### Phase 0: トリアージ
- コードベースサイズ判定（SMALL/MEDIUM/LARGE）
- 変更内容の抽出
- ファイル別リスクスコア

### Phase 1: 変更コード分析
- 両バージョンの読み込み
- 削除コードのGit blame
- リグレッションチェック
- マイクロ敵対的分析
- 攻撃シナリオ生成

### Phase 2: テストカバレッジ分析
- テストギャップの特定
- リスクエレベーションルール適用

### Phase 3: ブラストラジアス分析
- 呼び出し元カウント
- 優先度マトリクス（リスク × ブラストラジアス）

### Phase 4: 深掘りコンテキスト分析
- 関数フローのマッピング
- 呼び出し追跡
- 不変条件の特定
- Five Whys根本原因分析

### Phase 5: 敵対的分析（HIGH RISKのみ）
- 攻撃者モデル定義（WHO/WHAT/WHERE）
- 具体的な攻撃ベクトル特定
- 悪用可能性評価（EASY/MEDIUM/HARD）
- 完全な悪用シナリオ構築
- ベースラインとのクロス参照

### Phase 6: レポート生成
- マークダウンレポート
- ファイル/行参照
- 攻撃シナリオ
- 推奨事項

---

## 主要な発見

### 1. セキュリティレビューのベストプラクティス

**Trail of Bits方式**:
- リスク優先（認証、暗号、値転送、外部呼び出し）
- 証拠ベース（git履歴、行番号、攻撃シナリオ）
- アダプティブ（コードベースサイズに応じた深度調整）
- 正直（明示的なカバレッジ制限）
- 出力駆動（常にマークダウンレポート生成）

**Piebald-AI方式**:
- 2段階検証（検出 + フィルタリング）
- 17+のハード除外ルール
- 信頼度≥8/10のみ報告
- サブタスク並列化で効率化

### 2. ワークフローの重要性

**obra/superpowers方式**:
- レビュータイミングの明確化（タスク後、機能完成後、マージ前）
- YAGNI強制（実際の使用を確認）
- 技術的厳密性（形だけの同意を禁止）
- No Performative Agreement

### 3. AIコードの典型的問題（2026年）

- **エッジケース処理の弱さ**: AIはハッピーパスに強いが、極端な入力に弱い
- **サイレントフェイラー**: エラーを隠蔽する傾向
- **過剰実装**: YAGNI違反が多い

### 4. 効率化のための技術

- **アダプティブ深度**: コードベースサイズで戦略変更
- **スマートキャッシング**: 設定変更で全無効化
- **並列化**: 検証を並列実行で高速化
- **先例ベース評価**: 既知の安全パターンで誤検知削減

---

## Sources（参照元）

### 公式プラグイン
- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)

### 新規発見リポジトリ（スター数順）
- [obra/superpowers](https://github.com/obra/superpowers) - 48,935 ⭐
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - 4,310 ⭐
- [trailofbits/skills](https://github.com/trailofbits/skills) - 2,498 ⭐
- [nizos/tdd-guard](https://github.com/nizos/tdd-guard) - 1,747 ⭐
- [Gentleman-Programming/gentleman-guardian-angel](https://github.com/Gentleman-Programming/gentleman-guardian-angel) - 560 ⭐
- [bartolli/claude-code-typescript-hooks](https://github.com/bartolli/claude-code-typescript-hooks) - 167 ⭐
- [Veraticus/cc-tools](https://github.com/Veraticus/cc-tools) - 46 ⭐

### スキルコレクション
- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

### コミュニティプラグイン
- [matsengrp/plugins](https://github.com/matsengrp/plugins)
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)

### ベストプラクティス記事
- [Claude Code Best Practices for Local Code Review](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)
- [Edge Cases and Error Handling: Where AI Code Falls Short](https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/)
- [8 Best AI Code Review Tools That Catch Real Bugs in 2026](https://www.qodo.ai/blog/best-ai-code-review-tools-2026/)

---

**作成日**: 2026-02-10
**作成者**: Claude Sonnet 4.5
**総調査時間**: 約90分
**総リポジトリ数**: 14
**総観点数**: 50（30基本 + 20新規/拡張）
**総プロンプトファイル**: 12個保存

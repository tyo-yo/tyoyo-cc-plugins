# アダプティブレビュー深度 ⭐⭐⭐⭐⭐

**ID**: S05
**カテゴリ**: セキュリティ（高度）
**優先度**: Tier 2（推奨）
**信頼度基準**: コードベースサイズに応じた適応

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Differential Review Skill](https://github.com/trailofbits/skills/blob/main/differential-review/differential-review.md)

---

## 概要

コードベースのサイズに応じてレビューの深度を動的に調整し、効率と網羅性のバランスを最適化します。

小規模プロジェクトでは全依存関係を徹底的に分析し、大規模プロジェクトではクリティカルパスのみに焦点を当てることで、限られたリソースで最大の効果を発揮します。Trail of Bitsのセキュリティレビュー経験に基づく、実践的なアプローチです。

---

## チェック内容

### コードベースサイズの判定

変更されたファイルとその依存関係の総ファイル数で判定:

```bash
# 変更ファイル数をカウント
git diff --name-only HEAD~1 HEAD | wc -l

# 依存関係を含めた総ファイル数を推定
# （言語/プロジェクトに応じたツールを使用）
```

### サイズ別戦略

| サイズ | ファイル数 | 戦略 | アプローチ |
|--------|----------|------|-----------|
| **SMALL** | <20 | **DEEP** | 全依存関係を読み込み、完全なgit blame、全てのコールチェーンを追跡 |
| **MEDIUM** | 20-200 | **FOCUSED** | 1ホップの依存関係のみ、優先度の高いファイルに焦点、リスクベースのgit blame |
| **LARGE** | 200+ | **SURGICAL** | 変更ファイルのみ、クリティカルパスのみ追跡、HIGH RISKのみgit blame |

### SMALL戦略（<20ファイル）

**目標**: 完全な理解

- ✅ 全ての依存ファイルを読み込む
- ✅ 全ての削除コードでgit blameを実行
- ✅ 全てのコールチェーンを追跡
- ✅ システム全体の不変条件を特定
- ✅ 完全なデータフロー分析

**実行時間**: 30-60分

### MEDIUM戦略（20-200ファイル）

**目標**: 重要な問題を見逃さない

- ✅ 変更ファイル + 1ホップの依存関係のみ
- ✅ HIGH/MEDIUMリスクのファイルを優先
- ✅ セキュリティコミットからの削除のみgit blame
- ✅ 主要なコールパスのみ追跡
- ⚠️ トランジティブな依存は対象外

**実行時間**: 15-30分

### LARGE戦略（200+ファイル）

**目標**: クリティカルな問題のみ検出

- ✅ 変更ファイルのみ分析
- ✅ HIGH RISKのファイルのみ深掘り
- ✅ レッドフラグ（認証、暗号、外部呼び出し）に焦点
- ✅ セキュリティコミットからの削除のみgit blame
- ⚠️ 依存関係は明示的にリスクが高い場合のみ
- ⚠️ LOW/MEDIUMリスクは軽くスキャンのみ

**実行時間**: 10-15分

---

## 適用基準

### 使用する場合

- ✅ セキュリティレビュー時
- ✅ 時間制約がある場合
- ✅ リソース効率を重視する場合
- ✅ 大規模コードベース（100+ファイル）

### 使用しない場合

- ❌ 小規模で徹底的なレビューが可能な場合（常にDEEPを使用）
- ❌ クリティカルなセキュリティ修正（常にDEEPを使用）
- ❌ 時間制約がない場合

---

## 具体例

### シナリオ1: SMALL戦略（15ファイル変更）

```bash
# 変更されたファイル
git diff --name-only HEAD~1 HEAD
# 出力: 15 files

# 戦略: DEEP
# - 全15ファイルを読み込む
# - 各ファイルの依存関係を全て追跡（+30ファイル）
# - 全ての削除コードでgit blameを実行
# - 完全なコールグラフを構築
```

**実行**:
1. 全45ファイル（15変更 + 30依存）を読み込む
2. システム全体の不変条件を特定
3. 完全なデータフローを追跡
4. 全てのセキュリティリスクを評価

**実行時間**: 45分

---

### シナリオ2: MEDIUM戦略（80ファイル変更）

```bash
# 変更されたファイル
git diff --name-only HEAD~1 HEAD
# 出力: 80 files

# 戦略: FOCUSED
# - 80ファイルのうち、HIGH/MEDIUMリスクのみ分析（20ファイル）
# - 1ホップの依存関係のみ追跡（+40ファイル）
# - セキュリティコミットからの削除のみgit blame
```

**実行**:
1. リスク評価で20ファイルに絞り込む
2. 1ホップの依存関係（+40ファイル）のみ読み込む
3. 主要なコールパスのみ追跡
4. HIGH/MEDIUMリスクに焦点

**実行時間**: 25分

---

### シナリオ3: LARGE戦略（300ファイル変更）

```bash
# 変更されたファイル
git diff --name-only HEAD~1 HEAD
# 出力: 300 files

# 戦略: SURGICAL
# - 300ファイルのうち、HIGH RISKのみ分析（10ファイル）
# - 依存関係は追跡しない（変更ファイルのみ）
# - レッドフラグ（認証、暗号）に焦点
```

**実行**:
1. リスク評価で10ファイルに絞り込む（認証、暗号、外部呼び出し）
2. 変更ファイルのみ読み込む（依存関係は対象外）
3. レッドフラグのチェックのみ実行
4. 残り290ファイルは軽くスキャン

**実行時間**: 15分

---

## 実装ガイド

### ファイル数のカウント

```bash
# 変更ファイル数
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | wc -l)

# 戦略の決定
if [ $CHANGED_FILES -lt 20 ]; then
  STRATEGY="DEEP"
elif [ $CHANGED_FILES -lt 200 ]; then
  STRATEGY="FOCUSED"
else
  STRATEGY="SURGICAL"
fi

echo "Strategy: $STRATEGY"
```

### リスクベースのファイル優先順位付け

```python
# リスクレベルの判定
def calculate_risk_score(file_path):
    high_risk_patterns = [
        'auth', 'login', 'password', 'crypto', 'token',
        'payment', 'billing', 'external', 'api'
    ]
    medium_risk_patterns = [
        'validate', 'sanitize', 'permission', 'access',
        'session', 'user', 'admin'
    ]

    score = 0
    for pattern in high_risk_patterns:
        if pattern in file_path.lower():
            score += 10
    for pattern in medium_risk_patterns:
        if pattern in file_path.lower():
            score += 5

    return score

# ファイルをリスクスコアでソート
files = sorted(changed_files, key=calculate_risk_score, reverse=True)
```

---

## 2026年トレンド

大規模モノレポやマイクロサービスの普及により、アダプティブレビュー深度の重要性が増加:

- **モノレポの巨大化**: 単一リポジトリに1000+ファイルが一般的
- **限られたレビュー時間**: 迅速なイテレーションが求められる
- **リスクベースアプローチ**: 全てをレビューするのは現実的でない

効率的なレビュー戦略が、セキュリティ品質の鍵となっています。

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S06] 攻撃者モデリング
- [S08] ブラストラジアス分析
- [S09] ベースラインコンテキスト構築
- [S10] レッドフラグエスカレーション

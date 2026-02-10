# ブラストラジアス（影響範囲）分析 ⭐⭐⭐⭐

**ID**: S08
**カテゴリ**: セキュリティ（高度）
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Differential Review: Blast Radius Analysis](https://github.com/trailofbits/skills/blob/main/differential-review/differential-review.md)

---

## 概要

変更されたコードの影響範囲（呼び出し元の数）を定量的に評価し、リスクレベルと組み合わせて優先順位を決定します。

「ブラストラジアス」とは、1つの脆弱性が影響を及ぼす範囲の大きさを表す概念です。同じリスクレベルの脆弱性でも、呼び出し元が多いほど影響範囲が広く、優先度が高くなります。これにより、最も影響の大きい変更を優先的にレビューできます。

---

## チェック内容

### 呼び出し元カウント

変更された関数/メソッドの呼び出し元の数を定量的に測定:

```bash
# 関数の呼び出し元をカウント
git grep "function_name" | wc -l

# 特定ファイルでの呼び出し元をカウント
git grep "function_name" -- "*.py" | wc -l
```

### ブラストラジアスのレベル分類

| 呼び出し元の数 | ブラストラジアス | 説明 |
|--------------|----------------|------|
| 1-5 | **LOW** | 限定的な影響範囲 |
| 6-20 | **MEDIUM** | 中程度の影響範囲 |
| 21-50 | **HIGH** | 広範囲の影響 |
| 50+ | **CRITICAL** | システム全体に影響 |

### 優先度マトリクス

リスクレベルとブラストラジアスを組み合わせて優先度を決定:

```
優先度 = リスクレベル × ブラストラジアス

例:
- HIGH risk × 50 callers (CRITICAL) = TOP PRIORITY
- MEDIUM risk × 5 callers (LOW) = LOWER PRIORITY
- LOW risk × 100 callers (CRITICAL) = MEDIUM PRIORITY
```

### 優先度マトリクス表

| リスク \ BR | LOW (1-5) | MEDIUM (6-20) | HIGH (21-50) | CRITICAL (50+) |
|------------|-----------|--------------|-------------|---------------|
| **HIGH** | P2 | P1 | P0 | P0 (TOP) |
| **MEDIUM** | P3 | P2 | P1 | P1 |
| **LOW** | P4 | P3 | P2 | P2 |

- **P0**: 即座に対応（最優先）
- **P1**: 優先度高
- **P2**: 優先度中
- **P3**: 優先度低
- **P4**: 時間があれば対応

---

## 適用基準

### 使用する場合

- ✅ 共通関数・ユーティリティ変更
- ✅ ライブラリコードの変更
- ✅ MEDIUM以上のリスクの変更
- ✅ 大規模リファクタリング
- ✅ 複数ファイルにまたがる変更

### 使用しない場合

- ❌ 呼び出し元がない（未使用コード）
- ❌ LOW RISKかつ呼び出し元が少ない（1-5）
- ❌ プライベート関数（内部実装のみ）

---

## 具体例

### 例1: HIGH RISK × CRITICAL BR = P0（最優先）

**変更内容**:
```python
# 認証チェック関数を変更
def is_authenticated(token):
-    return verify_signature(token) and check_expiry(token)
+    return check_expiry(token)  # 署名検証を削除（脆弱）
```

**ブラストラジアス分析**:
```bash
# 呼び出し元をカウント
git grep "is_authenticated" | wc -l
# 出力: 87
```

**評価**:
- **リスクレベル**: HIGH（認証バイパス）
- **ブラストラジアス**: CRITICAL（87呼び出し元）
- **優先度**: P0（最優先）
- **影響**: システム全体の認証が無効化される可能性

---

### 例2: MEDIUM RISK × LOW BR = P3（優先度低）

**変更内容**:
```python
# ログフォーマット関数を変更
def format_log_message(message):
-    return f"[{datetime.now()}] {escape_html(message)}"
+    return f"[{datetime.now()}] {message}"  # サニタイゼーション削除
```

**ブラストラジアス分析**:
```bash
# 呼び出し元をカウント
git grep "format_log_message" | wc -l
# 出力: 3
```

**評価**:
- **リスクレベル**: MEDIUM（ログインジェクションの可能性）
- **ブラストラジアス**: LOW（3呼び出し元、内部のみ）
- **優先度**: P3（優先度低）

---

## 実装ガイド

### 自動ブラストラジアス計算

```python
# blast_radius_analysis.py

import subprocess

def count_callers(function_name, file_extension="*.py"):
    """関数の呼び出し元をカウント"""
    result = subprocess.run(
        ["git", "grep", function_name, "--", file_extension],
        capture_output=True,
        text=True
    )
    return len(result.stdout.strip().split('\n')) if result.stdout else 0

def classify_blast_radius(count):
    """ブラストラジアスを分類"""
    if count <= 5:
        return "LOW"
    elif count <= 20:
        return "MEDIUM"
    elif count <= 50:
        return "HIGH"
    else:
        return "CRITICAL"

def calculate_priority(risk_level, blast_radius):
    """優先度を計算"""
    priority_matrix = {
        ("HIGH", "LOW"): "P2",
        ("HIGH", "MEDIUM"): "P1",
        ("HIGH", "HIGH"): "P0",
        ("HIGH", "CRITICAL"): "P0",
        ("MEDIUM", "LOW"): "P3",
        ("MEDIUM", "MEDIUM"): "P2",
        ("MEDIUM", "HIGH"): "P1",
        ("MEDIUM", "CRITICAL"): "P1",
        ("LOW", "LOW"): "P4",
        ("LOW", "MEDIUM"): "P3",
        ("LOW", "HIGH"): "P2",
        ("LOW", "CRITICAL"): "P2",
    }
    return priority_matrix.get((risk_level, blast_radius), "P4")

# 使用例
function_name = "is_authenticated"
caller_count = count_callers(function_name)
blast_radius = classify_blast_radius(caller_count)
priority = calculate_priority("HIGH", blast_radius)

print(f"Function: {function_name}")
print(f"Caller Count: {caller_count}")
print(f"Blast Radius: {blast_radius}")
print(f"Priority: {priority}")
```

---

## 2026年トレンド

大規模なモノレポやマイクロサービスアーキテクチャの普及により、ブラストラジアス分析の重要性が増加:

- **共通ライブラリの肥大化**: 1つの変更が数百のサービスに影響
- **トランジティブな依存**: 直接の呼び出し元だけでなく、間接的な影響も考慮が必要
- **マイクロサービス間の依存**: APIの変更が複数のサービスに波及

定量的な影響範囲の評価が、効率的なレビュー戦略の鍵となっています。

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S05] アダプティブレビュー深度
- [S06] 攻撃者モデリング
- [S07] セキュリティリグレッション
- [S10] レッドフラグエスカレーション
- [D04] 依存関係管理

# セキュリティリグレッション ⭐⭐⭐⭐⭐

**ID**: S07
**カテゴリ**: セキュリティ（高度）
**優先度**: Tier 2（推奨）
**信頼度基準**: 91-100点

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Differential Review: Security Regression Detection](https://github.com/trailofbits/skills/blob/main/differential-review/differential-review.md)

---

## 概要

過去に修正されたセキュリティ脆弱性が、新しいコード変更によって再発していないかをGit履歴ベースで検出します。

特に、セキュリティコミット（"security", "CVE", "fix"等を含むコミット）から削除されたコードが、新しいコードで再導入されていないかを自動的にチェックします。これにより、意図しないセキュリティリグレッションを早期に発見できます。

---

## チェック内容

### Git履歴ベースの検出

#### 1. セキュリティコミットの特定

```bash
# セキュリティ関連コミットを検索
git log --grep="security\|CVE\|vulnerability\|fix" --all --oneline
```

#### 2. 削除されたコードの検出

```bash
# セキュリティコミットで削除されたコードを確認
git show <security-commit> | grep "^-" | grep -v "^---"
```

#### 3. 再導入の検出

```bash
# 現在のコードに同じパターンが存在するか確認
git diff <security-commit> HEAD -- <file>
```

### チェック対象

#### 認証・認可の削除
- 認証チェックの削除
- 権限検証の削除
- アクセス制御修飾子の削除（private → public）
- セッション検証の削除

#### バリデーションの削除
- 入力検証の削除
- サニタイゼーション処理の削除
- 境界値チェックの削除
- 型チェックの削除

#### セキュリティ設定の削除
- HTTPS強制の削除
- CSRF保護の削除
- セキュアフラグの削除（httpOnly, secure）
- Content-Security-Policy設定の削除

#### 暗号化処理の削除
- 暗号化処理の削除
- ハッシュ化処理の削除
- 署名検証の削除

---

## 適用基準

### 使用する場合

- ✅ セキュリティ関連コード変更
- ✅ 過去にCVE修正があるファイルの変更
- ✅ 認証・認可ロジックの変更
- ✅ リファクタリング（意図しない削除の可能性）
- ✅ 大規模な変更（削除行数が多い場合）

### 使用しない場合

- ❌ 新規ファイル追加（過去の履歴がない）
- ❌ ドキュメント変更のみ
- ❌ セキュリティに無関係なコード変更

---

## 具体例

### 例1: 認証チェックの削除（リグレッション検出）

**過去のセキュリティ修正コミット（abc1234）**:
```python
# コミットメッセージ: "security: add authentication check to admin endpoint"

# 修正後（安全）
@app.route('/admin/users')
+@login_required
+@admin_required
def admin_users():
    return User.query.all()
```

**現在の変更（リグレッション）**:
```python
# リファクタリング中に誤って認証チェックを削除
@app.route('/admin/users')
-@login_required
-@admin_required
def admin_users():
    return User.query.all()
```

**評価**:
- **リスクレベル**: HIGH（認証バイパス）
- **信頼度**: 10/10（明確なリグレッション）
- **推奨**: 即座に修正、セキュリティコミットの意図を再確認

---

### 例2: バリデーションの削除（リグレッション検出）

**過去のセキュリティ修正コミット（def5678）**:
```javascript
// コミットメッセージ: "CVE-2023-12345: prevent XSS in user profile"

// 修正後（安全）
function renderUserProfile(username) {
+  const sanitized = sanitizeHtml(username);
+  return `<h1>Welcome, ${sanitized}!</h1>`;
}
```

**現在の変更（リグレッション）**:
```javascript
// パフォーマンス改善のつもりで、サニタイゼーションを削除
function renderUserProfile(username) {
-  const sanitized = sanitizeHtml(username);
-  return `<h1>Welcome, ${sanitized}!</h1>`;
+  return `<h1>Welcome, ${username}!</h1>`;
}
```

**評価**:
- **リスクレベル**: HIGH（XSS脆弱性の再発）
- **信頼度**: 10/10（CVE修正の巻き戻し）
- **推奨**: 即座に修正、CVE-2023-12345の再確認

---

## 実装ガイド

### 自動検出スクリプト

```bash
#!/bin/bash
# security-regression-check.sh

# セキュリティコミットを取得
SECURITY_COMMITS=$(git log --grep="security\|CVE\|vulnerability\|fix" --all --oneline | cut -d' ' -f1)

echo "=== Security Regression Check ==="
echo ""

for commit in $SECURITY_COMMITS; do
  echo "Checking commit: $commit"

  # 変更されたファイルを取得
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

  for file in $CHANGED_FILES; do
    # セキュリティコミットからの差分を確認
    DIFF=$(git diff $commit HEAD -- $file 2>/dev/null)

    if [ -n "$DIFF" ]; then
      # 削除された行を確認
      REMOVED_LINES=$(echo "$DIFF" | grep "^-" | grep -v "^---")

      if [ -n "$REMOVED_LINES" ]; then
        echo "  ⚠️  Potential regression in $file:"
        echo "$REMOVED_LINES"
        echo ""
      fi
    fi
  done
done
```

---

## 2026年トレンド

AI生成コードによるリファクタリングが一般化した結果、意図しないセキュリティリグレッションが増加:

- **コンテキスト不足**: AIが過去のセキュリティ修正の意図を理解していない
- **過剰な最適化**: パフォーマンス改善のつもりで重要な検証を削除
- **不完全な移植**: コードを別の場所に移動した際、セキュリティチェックが漏れる

Git履歴ベースの自動検出が、セキュリティ品質維持の鍵となっています。

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S02] 一般的な脆弱性パターン
- [S06] 攻撃者モデリング
- [S10] レッドフラグエスカレーション
- [CTX01] Git履歴分析

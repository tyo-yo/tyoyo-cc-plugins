# レッドフラグエスカレーション ⭐⭐⭐⭐⭐

**ID**: S10
**カテゴリ**: セキュリティ（高度）
**優先度**: Tier 2（推奨）
**信頼度基準**: 100点（即座エスカレーション）

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Differential Review: Red Flag Escalation](https://github.com/trailofbits/skills/blob/main/differential-review/differential-review.md)

---

## 概要

重大なセキュリティリスクを示す「レッドフラグ」を検出した瞬間、他のチェックをスキップして即座にエスカレーションします。

レッドフラグは、過去のセキュリティインシデントや監査経験に基づく、明確かつ深刻なリスクパターンです。これらを検出した場合、通常のレビューフローを中断し、直ちにセキュリティチームやシニアエンジニアに報告する必要があります。

---

## チェック内容

### レッドフラグのカテゴリ

#### 1. セキュリティコミットからのコード削除

過去にセキュリティ修正として追加されたコードが削除されている場合:

```bash
# セキュリティコミットからの削除を検出
git log --grep="security\|CVE\|vulnerability" --all --oneline
git diff <security-commit> HEAD -- <file>

# 削除行に認証、検証、暗号化関連のキーワードが含まれる
grep "^-" | grep "auth\|verify\|validate\|encrypt\|sanitize"
```

**例**:
- 認証チェックの削除
- 署名検証の削除
- 入力バリデーションの削除
- 暗号化処理の削除

#### 2. アクセス制御修飾子の削除

アクセス制御が緩和される変更:

```python
# 悪い例
-@admin_required
 def delete_user(user_id):

# または
-    private void processPayment()
+    public void processPayment()
```

**影響**: 認証バイパス、権限昇格

#### 3. 検証の削除（置換なし）

検証処理が削除され、代替の検証が追加されていない場合:

```python
# 悪い例
-    if not validate_input(user_input):
-        raise ValidationError("Invalid input")
     return process_data(user_input)
```

**影響**: SQLインジェクション、XSS、コマンドインジェクション

#### 4. 外部呼び出しの追加（検証なし）

外部システムへの呼び出しが、適切な検証なしで追加される場合:

```python
# 悪い例
+    response = requests.get(f"https://api.example.com/{user_input}")
```

**影響**: SSRF（Server-Side Request Forgery）、データ漏洩

#### 5. 高ブラストラジアス（50+）+ HIGH リスク

呼び出し元が50以上かつHIGH RISKの変更:

```bash
# 呼び出し元カウント
git grep "authenticate_user" | wc -l
# 出力: 87

# HIGH RISKの変更（認証ロジック変更）
```

**影響**: システム全体に影響する重大な脆弱性

#### 6. 暗号化アルゴリズムの弱体化

強力な暗号化から弱い暗号化への変更:

```python
# 悪い例
-    hash = bcrypt.hashpw(password, bcrypt.gensalt())
+    hash = hashlib.md5(password.encode()).hexdigest()
```

**影響**: パスワードクラッキング、データ漏洩

#### 7. 認証情報のハードコード

認証情報が環境変数からハードコードに変更される場合:

```python
# 悪い例
-    api_key = os.environ.get('API_KEY')
+    api_key = "sk_live_abc123xyz789"
```

**影響**: 認証情報の露出、不正アクセス

---

## 適用基準

### 使用する場合

- ✅ セキュリティ関連コード変更
- ✅ 過去にCVE修正があるファイルの変更
- ✅ 認証・認可ロジックの変更
- ✅ 暗号化処理の変更
- ✅ 外部API呼び出しの追加

### 使用しない場合

- ❌ LOW RISKの変更（ドキュメント、テストのみ）
- ❌ セキュリティに無関係なコード変更

---

## 具体例

### 例1: セキュリティコミットからの削除（レッドフラグ）

**過去のセキュリティコミット（abc1234）**:
```python
# コミットメッセージ: "security: add authentication check to admin endpoint"

# 修正後（安全）
@app.route('/admin/users')
+@login_required
+@admin_required
def admin_users():
    return User.query.all()
```

**現在の変更（レッドフラグ）**:
```python
# 認証チェックを削除
@app.route('/admin/users')
-@login_required
-@admin_required
def admin_users():
    return User.query.all()
```

**エスカレーション**:
```
🚨 RED FLAG DETECTED 🚨

Category: Security commit code removal
File: app.py
Line: 42-43
Severity: CRITICAL
Risk Level: HIGH
Blast Radius: CRITICAL (87 callers)

Description:
Authentication decorators removed from admin endpoint.
This code was added in security commit abc1234 to prevent authentication bypass.

Impact:
- Admin endpoint is now accessible without authentication
- System-wide authentication compromise

Recommendation:
IMMEDIATELY revert this change and consult security team.

Previous Security Commit:
abc1234 - "security: add authentication check to admin endpoint"
```

---

### 例2: アクセス制御修飾子の削除（レッドフラグ）

**変更前**:
```python
@app.route('/api/users/<user_id>/delete', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {'status': 'success'}
```

**変更後（レッドフラグ）**:
```python
@app.route('/api/users/<user_id>/delete', methods=['DELETE'])
-@admin_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {'status': 'success'}
```

**エスカレーション**:
```
🚨 RED FLAG DETECTED 🚨

Category: Access control modifier removal
File: api/users.py
Line: 42
Severity: CRITICAL
Risk Level: HIGH

Description:
Admin required decorator removed from user deletion endpoint.
Any authenticated user can now delete any other user.

Impact:
- Privilege escalation (user → admin)
- Data loss (unauthorized user deletion)

Recommendation:
IMMEDIATELY revert this change. If removal is intentional,
add alternative authorization check and document in commit message.
```

---

## 実装ガイド

### 自動レッドフラグ検出

```bash
#!/bin/bash
# red_flag_detection.sh

RED_FLAGS=0

echo "=== Red Flag Detection ==="
echo ""

# 1. セキュリティコミットからの削除
SECURITY_COMMITS=$(git log --grep="security\|CVE\|vulnerability\|fix" --all --oneline | cut -d' ' -f1)

for commit in $SECURITY_COMMITS; do
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

  for file in $CHANGED_FILES; do
    DIFF=$(git diff $commit HEAD -- $file 2>/dev/null)
    REMOVED_LINES=$(echo "$DIFF" | grep "^-" | grep "auth\|verify\|validate\|encrypt\|sanitize")

    if [ -n "$REMOVED_LINES" ]; then
      echo "🚨 RED FLAG: Security commit code removal"
      echo "  File: $file"
      echo "  Commit: $commit"
      echo "  Removed: $REMOVED_LINES"
      echo ""
      RED_FLAGS=$((RED_FLAGS + 1))
    fi
  done
done

# 2. アクセス制御修飾子の削除
DIFF=$(git diff HEAD~1 HEAD)
REMOVED_AUTH=$(echo "$DIFF" | grep "^-" | grep "@admin_required\|@login_required\|@require_permission")

if [ -n "$REMOVED_AUTH" ]; then
  echo "🚨 RED FLAG: Access control modifier removal"
  echo "$REMOVED_AUTH"
  echo ""
  RED_FLAGS=$((RED_FLAGS + 1))
fi

# 3. 検証の削除
REMOVED_VALIDATION=$(echo "$DIFF" | grep "^-" | grep "validate\|sanitize\|clean")

if [ -n "$REMOVED_VALIDATION" ]; then
  echo "🚨 RED FLAG: Validation removal"
  echo "$REMOVED_VALIDATION"
  echo ""
  RED_FLAGS=$((RED_FLAGS + 1))
fi

# 結果
if [ $RED_FLAGS -gt 0 ]; then
  echo "=== $RED_FLAGS RED FLAG(S) DETECTED ==="
  echo "IMMEDIATE ACTION REQUIRED"
  exit 1
else
  echo "No red flags detected."
  exit 0
fi
```

---

## 2026年トレンド

AI生成コードによるリファクタリングが一般化し、意図しないレッドフラグが増加:

- **コンテキスト不足**: AIが過去のセキュリティ修正の意図を理解していない
- **過剰な最適化**: パフォーマンス改善のつもりで重要な検証を削除
- **不完全な移植**: コードを別の場所に移動した際、セキュリティチェックが漏れる

レッドフラグの自動検出が、セキュリティ品質維持の最後の砦となっています。

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S05] アダプティブレビュー深度
- [S06] 攻撃者モデリング
- [S07] セキュリティリグレッション
- [S08] ブラストラジアス分析
- [CTX01] Git履歴分析

# 先例ベースの評価

**ID**: S04
**カテゴリ**: セキュリティ（基本）
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Security Review Command](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/security-review.md)

---

## 概要

既存のコードベース内で「安全」と認識されているパターンを学習し、同様のパターンを誤検知として扱わないようにします。

プロジェクト固有のセキュリティパターンや、過去のレビューで「安全」と判断された実装方法を先例として参照することで、コンテキストに沿ったレビューを実現します。これにより、プロジェクトの慣習を理解した上での適切な評価が可能になります。

---

## チェック内容

### 先例の収集

- 過去のセキュリティレビューで承認されたパターン
- プロジェクト内で広く使用されている実装方法
- セキュリティ関連のコミット履歴から抽出されたパターン
- フレームワーク/ライブラリの推奨パターン

### 信頼されたパターンの例

#### XSS対策
- React.createElement()
- Angular sanitizer
- Vue.jsテンプレート
- Jinja2自動エスケープ
- フレームワーク提供のサニタイザー

#### インジェクション対策
- パラメータ化クエリ（Prepared Statements）
- ORM（Sequelize、TypeORM、SQLAlchemy）
- 安全なテンプレートエンジン

#### シークレット管理
- process.env.*（環境変数）
- Vault API
- AWS Secrets Manager
- Kubernetes Secrets

### 新しいパターンの評価

新しいコード変更を既存の安全なパターンと比較:

1. **完全一致**: 既知の安全パターンと同一 → 安全
2. **類似**: 既知パターンの変形 → 詳細検証
3. **逸脱**: 既知パターンと異なる → 高リスク

---

## 適用基準

### 使用する場合

- ✅ 既存の安全パターンが存在する場合
- ✅ プロジェクトに独自のセキュリティ慣習がある場合
- ✅ 類似コードが過去に承認されている場合
- ✅ フレームワーク固有のセキュリティパターンがある場合

### 使用しない場合

- ❌ 新規プロジェクト（先例が存在しない）
- ❌ 先例が不適切な可能性がある場合
- ❌ セキュリティ標準の見直し中

---

## 具体例

### ✅ 先例に基づく安全判定: React

```javascript
// プロジェクト内で広く使用されている安全なパターン
// 既存コード（承認済み）
function UserGreeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

// 新しいコード（先例に一致）
function WelcomeMessage({ username }) {
  return <p>Welcome back, {username}!</p>;
}
```

**評価**: 既存の承認済みパターンと一致するため、安全と判定。

---

### ✅ 先例に基づく安全判定: データベースアクセス

```python
# 既存コード（承認済み）
def get_user_by_id(user_id):
    return db.session.query(User).filter_by(id=user_id).first()

# 新しいコード（先例に一致）
def get_order_by_id(order_id):
    return db.session.query(Order).filter_by(id=order_id).first()
```

**評価**: ORMを使用したパラメータ化クエリで、既存パターンと一致するため安全。

---

### ⚠️ 先例からの逸脱: 生SQL使用

```python
# 既存コード（承認済み）
def get_user_by_id(user_id):
    return db.session.query(User).filter_by(id=user_id).first()

# 新しいコード（先例から逸脱）
def get_user_by_name(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

**評価**: 既存パターン（ORM）と異なり、生SQLを直接使用しているため、SQLインジェクションのリスクあり。
**信頼度**: 9/10

---

### ✅ 先例に基づく安全判定: シークレット管理

```python
# 既存コード（承認済み）
import os
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')

# 新しいコード（先例に一致）
import os
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
```

**評価**: 環境変数からシークレットを取得する既存パターンと一致するため安全。

---

## 2026年トレンド

AI生成コードでは、プロジェクト固有の慣習を無視して、汎用的なパターンを適用する傾向があります:

- **フレームワークの無視**: プロジェクトで使用しているフレームワークの安全機能を活用しない
- **既存パターンの不一致**: 同じ機能を異なる方法で実装してしまう
- **過剰な汎用性**: プロジェクト固有の最適化を無視した実装

先例ベースの評価により、プロジェクトの一貫性を保ちつつ、セキュリティを確保できます。

---

## 実装ガイド

### 先例パターンの抽出

```bash
# セキュリティ関連の承認済みコミットを検索
git log --grep="security|auth|sanitize" --all --oneline

# 特定ファイルでの安全なパターンを抽出
git show <commit>:<file> | grep -A 5 "sanitize\|escape\|parameterized"
```

### 先例データベースの構築

プロジェクト内で以下を文書化:

1. **認証パターン**: プロジェクトで使用する認証方法
2. **データベースアクセス**: ORMの使用方法
3. **入力検証**: バリデーションライブラリの使用方法
4. **シークレット管理**: 環境変数、Vault等の使用方法
5. **XSS対策**: フレームワークのサニタイザー使用方法

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S02] 一般的な脆弱性パターン
- [S03] False Positiveフィルタリング
- [S09] ベースラインコンテキスト構築

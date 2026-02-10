# ベースラインコンテキスト構築

**ID**: S09
**カテゴリ**: セキュリティ（高度）
**優先度**: Tier 3（オプション）
**信頼度基準**: 前処理（スコアリングなし）

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Audit Context Building Skill](https://github.com/trailofbits/skills/blob/main/audit-context-building/audit-context-building.md)

---

## 概要

システム全体のセキュリティコンテキスト（不変条件、信頼境界、検証パターン）を事前に構築し、個別のレビューで参照できるようにします。

ベースラインコンテキストは、プロジェクト全体のセキュリティポリシーと実装パターンを文書化したもので、差分レビュー時に「既存の安全パターンからの逸脱」を検出するための基準となります。初回レビューや大規模セキュリティレビューで特に有効です。

---

## チェック内容

### システム全体の不変条件

システム全体で常に成立すべきセキュリティ条件:

#### 認証・認可
- **不変条件**: 全ての管理者エンドポイントは認証デコレータで保護される
- **検証方法**: git grepで管理者エンドポイントをチェック
- **例外**: なし

#### データ完全性
- **不変条件**: ユーザー入力は常にバリデーション後に使用される
- **検証方法**: 入力受信箇所とバリデーション呼び出しの対応を確認
- **例外**: 信頼された内部データ（環境変数、設定ファイル）

#### 暗号化
- **不変条件**: パスワードは必ず適切なハッシュアルゴリズムでハッシュ化される
- **検証方法**: パスワード処理箇所をチェック
- **例外**: 一時的なパスワードリセットトークン（有効期限付き）

### 信頼境界の定義

データの信頼レベルを明確化:

```
[信頼されない] ← [検証層] → [信頼される]

例:
- ユーザー入力（HTTP request） → バリデーション → アプリケーションロジック
- 外部API → サニタイゼーション → データベース
- ファイルアップロード → ウイルススキャン → ストレージ
```

#### 信頼境界のチェックポイント
- **境界の明確化**: 信頼されないデータが信頼される領域に入る箇所
- **検証の実施**: 境界で適切なバリデーション/サニタイゼーションが実施されているか
- **防御の多層化**: 1つの境界だけでなく、複数の防御層があるか

### 検証パターンのカタログ

プロジェクト内で使用される検証パターンを文書化:

#### 入力検証
```python
# パターン1: スキーマバリデーション
from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate_username)
    email = fields.Email(required=True)

# パターン2: 型チェック
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
```

#### SQLインジェクション対策
```python
# パターン1: ORMの使用
user = db.session.query(User).filter_by(username=username).first()

# パターン2: パラメータ化クエリ
db.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### コールグラフの構築

主要な関数の呼び出し関係を可視化:

```
[User Input] → validate_input() → process_data() → save_to_db()
                    ↓                    ↓
              ValidationError      sanitize_html()
```

---

## 適用基準

### 使用する場合

- ✅ 初回レビュー時（プロジェクトの理解）
- ✅ 大規模セキュリティレビュー
- ✅ 新しいチームメンバーのオンボーディング
- ✅ セキュリティ監査の準備
- ✅ プロジェクト全体のリファクタリング前

### 使用しない場合

- ❌ 小規模な変更のレビュー（オーバーヘッドが大きい）
- ❌ 既にベースラインが存在する場合（更新のみ）
- ❌ 時間制約が厳しい場合

---

## 具体例

### 例1: 認証の不変条件

**ベースラインコンテキスト**:
```markdown
## 認証の不変条件

### ルール
全ての管理者エンドポイント（/admin/*）は認証デコレータで保護される。

### 検証方法
git grepで管理者エンドポイントを検索し、認証デコレータの有無を確認。

### 例外
なし（全ての管理者エンドポイントは認証必須）
```

**レビュー時の活用**:
```python
# 新しいコード
@app.route('/admin/users')
def admin_users():
    return User.query.all()
```

**評価**:
- **不変条件違反**: 認証デコレータがない
- **リスクレベル**: HIGH（認証バイパス）
- **推奨**: 認証デコレータを追加

---

### 例2: 信頼境界の定義

**ベースラインコンテキスト**:
```markdown
## 信頼境界

### 境界1: HTTP Request → Application Logic
- **バリデーション**: marshmallowスキーマでバリデーション
- **場所**: api/schemas.py
- **例外**: 内部API（/internal/*）は信頼されたサービスからのみアクセス

### 境界2: Application Logic → Database
- **サニタイゼーション**: ORMのパラメータ化クエリを使用
- **場所**: models/*.py
- **例外**: なし
```

**レビュー時の活用**:
```python
# 新しいコード
@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    # バリデーションなしで直接使用（信頼境界違反）
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
```

**評価**:
- **信頼境界違反**: HTTP Request → Application Logicの境界でバリデーションが欠如
- **リスクレベル**: MEDIUM（不正なデータが保存される可能性）
- **推奨**: marshmallowスキーマでバリデーションを追加

---

## 実装ガイド

### ベースラインコンテキストの構築手順

#### 1. 不変条件の抽出

```bash
# 認証関連のパターンを抽出
git grep "@login_required\|@admin_required" | cut -d: -f1 | sort | uniq

# 暗号化関連のパターンを抽出
git grep "bcrypt\|hashlib\|crypto" | cut -d: -f1 | sort | uniq
```

#### 2. 信頼境界の特定

```bash
# ユーザー入力の受信箇所
git grep "request.json\|request.args\|request.form"

# バリデーション実施箇所
git grep "validate\|schema\|clean"
```

#### 3. 検証パターンのカタログ化

プロジェクト内で使用されている検証パターンを文書化:

```markdown
## 検証パターン

### 入力検証
- **パターン1**: Marshmallowスキーマ（api/schemas.py）
- **パターン2**: Pydanticモデル（models/validators.py）

### SQLインジェクション対策
- **パターン1**: SQLAlchemy ORM（models/*.py）
- **パターン2**: パラメータ化クエリ（db/queries.py）
```

---

## 2026年トレンド

大規模プロジェクトやマイクロサービスの普及により、ベースラインコンテキストの重要性が増加:

- **コンテキストの共有**: チーム間でセキュリティポリシーを共有
- **自動化**: ベースラインコンテキストの自動構築ツールの普及
- **継続的更新**: CI/CDでベースラインコンテキストを自動更新

プロジェクト全体のセキュリティ理解が、効率的なレビューの基盤となっています。

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S04] 先例ベースの評価
- [S05] アダプティブレビュー深度
- [S07] セキュリティリグレッション
- [CTX02] コードベース理解

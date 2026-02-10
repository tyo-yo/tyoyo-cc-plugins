# アンチパターン

**ID**: Q04
**カテゴリ**: 品質と保守性
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [matsengrp/plugins - antipattern-scanner](https://github.com/matsengrp/plugins)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

アンチパターンは、一見良さそうに見えるが実際には保守性、拡張性、パフォーマンスを著しく低下させる設計パターンです。これらは長期的なコストを増加させ、バグの温床となります。本観点では、言語非依存の汎用的なアンチパターンを検出し、より良い設計へのリファクタリングを提案します。

---

## チェック内容

- God Object（神オブジェクト）: すべての責務を持つ巨大なクラス
- Spaghetti Code（スパゲッティコード）: 構造化されていない複雑な制御フロー
- Lava Flow（溶岩流）: 使われなくなったコードの残存
- Golden Hammer（黄金のハンマー）: 特定技術への過度な依存
- Cargo Cult Programming（カーゴカルト）: 理解せずにコピーしたコード
- Premature Optimization（早すぎる最適化）: 実際の問題前の最適化
- Shotgun Surgery（ショットガン手術）: 1つの変更に多数ファイルの修正が必要
- Divergent Change（発散的変更）: 1つのクラスが複数の理由で変更される

---

## 適用基準

### 使用する場合

- ✅ アーキテクチャ変更
- ✅ 大規模実装
- ✅ 複雑なロジックの追加
- ✅ 新規モジュール追加

### 使用しない場合

- ❌ 単純なバグ修正
- ❌ ドキュメント変更のみ
- ❌ テストコードのみの変更

---

## 具体例

### ❌ 悪い例: God Object

```python
class UserManager:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.email_service = EmailService()
        self.payment_processor = PaymentProcessor()

    def create_user(self, data):
        # ユーザー作成
        pass

    def authenticate_user(self, credentials):
        # 認証処理
        pass

    def process_payment(self, user_id, amount):
        # 支払い処理
        pass

    def send_notification(self, user_id, message):
        # 通知送信
        pass

    def generate_report(self, user_id):
        # レポート生成
        pass

    def export_data(self, format):
        # データエクスポート
        pass
```

**問題点**: 1つのクラスが認証、支払い、通知、レポート生成など多数の責務を持ち、単一責任の原則に違反しています。

### ✅ 良い例: 責務の分離

```python
class UserRepository:
    def create_user(self, data):
        # ユーザー作成のみ
        pass

class AuthenticationService:
    def authenticate(self, credentials):
        # 認証処理のみ
        pass

class PaymentService:
    def process_payment(self, user_id, amount):
        # 支払い処理のみ
        pass

class NotificationService:
    def send(self, user_id, message):
        # 通知送信のみ
        pass
```

**理由**: 各クラスが単一の責務を持ち、変更の影響範囲が限定されます。

---

### ❌ 悪い例: Lava Flow（使われないコード）

```typescript
class OrderProcessor {
  // 新しい実装
  processOrder(order: Order): Result {
    return this.newProcessingLogic(order);
  }

  // 古い実装（使われていない）
  processOrderOld(order: Order): Result {
    // 古いロジック
    return oldLogic(order);
  }

  // さらに古い実装（使われていない）
  processOrderLegacy(order: Order): Result {
    // レガシーロジック
    return legacyLogic(order);
  }
}
```

**問題点**: 使われなくなった古いメソッドが残存し、コードベースを複雑化しています。

### ✅ 良い例: 不要コードの削除

```typescript
class OrderProcessor {
  processOrder(order: Order): Result {
    return this.newProcessingLogic(order);
  }
}
```

**理由**: 使われていないコードを削除することで、保守性が向上し、混乱を防ぎます。

---

### ❌ 悪い例: Shotgun Surgery

```javascript
// user.js
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.status = 'active'; // 新フィールド追加時に修正
  }
}

// userController.js
function createUser(req, res) {
  const user = new User(req.body.name, req.body.email);
  user.status = 'active'; // 修正必要
  db.save(user);
}

// userService.js
function updateUser(id, data) {
  const user = db.find(id);
  user.name = data.name;
  user.email = data.email;
  user.status = data.status || 'active'; // 修正必要
  return user;
}

// userValidator.js
function validateUser(userData) {
  return userData.name && userData.email && userData.status; // 修正必要
}
```

**問題点**: `status`フィールドの追加に伴い、複数ファイルの修正が必要になっています。

### ✅ 良い例: カプセル化

```javascript
// user.js
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.status = 'active';
  }

  static create(name, email) {
    return new User(name, email);
  }

  isValid() {
    return this.name && this.email && this.status;
  }
}

// userController.js
function createUser(req, res) {
  const user = User.create(req.body.name, req.body.email);
  db.save(user);
}
```

**理由**: ユーザーの生成ロジックとバリデーションをUserクラスにカプセル化し、変更の影響範囲を限定しています。

---

## 2026年トレンド

AIコード生成ツールは、短期的には動作するコードを生成できますが、長期的な保守性を考慮した設計パターンの選択は苦手です。特に以下のアンチパターンがAI生成コードに頻出します。

- Cargo Cult Programming: 他のコードベースからのコピー＆ペースト
- Premature Optimization: 実際のパフォーマンス問題がない段階での複雑な最適化
- God Object: すべての機能を1つのクラスにまとめる傾向

---

## 関連観点

- [Q03] コード臭
- [Q02] 複雑性
- [D02] アーキテクチャパターン準拠
- [Q01] 読みやすさ

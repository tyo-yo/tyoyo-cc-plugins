# 機能要件の適合性

**ID**: C02
**カテゴリ**: 正確性（基本）
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点

---

## 参照元

- 新規観点（業界ベストプラクティスより）

---

## 概要

この観点は、実装が意図された機能要件を満たしているかを確認します。PRの説明、コミットメッセージ、Issue、仕様書に記載された要求事項が正しく実装されているかをチェックし、機能不足や誤実装を防ぎます。

新機能追加や機能変更の際に適用し、ビジネスロジックが正確に実装されていることを保証します。

---

## チェック内容

- PRの説明に記載された機能の実現
  - 記載された全ての機能が実装されているか
  - 実装範囲が説明と一致しているか
- ビジネスロジックの正確性
  - 計算ロジックの正確性
  - 状態遷移の正しさ
  - ワークフローの完全性
- ユーザーストーリーの達成
  - Acceptance Criteriaの充足
  - ユーザーシナリオの実現
- 期待される入出力の一致
  - 入力パラメータの型と値の範囲
  - 出力形式とデータ構造
  - エラーケースのハンドリング
- 仕様書との整合性
  - API仕様書との一致
  - データモデルの正確性
  - 画面仕様との一致
- 暗黙の要件の考慮
  - パフォーマンス要件
  - セキュリティ要件
  - アクセシビリティ要件

---

## 適用基準

### 使用する場合

- ✅ 新機能追加
- ✅ 機能変更
- ✅ ビジネスロジックの修正
- ✅ API仕様の実装

### 使用しない場合

- ❌ リファクタリングのみ（機能変更なし）
- ❌ コメント・ドキュメント変更のみ
- ❌ テストコードのみの追加

---

## 具体例

### ❌ 悪い例：機能不足

```typescript
// PR説明: "ユーザーが商品を購入できるようにする。在庫チェック、決済処理、注文履歴への記録を含む"

async function purchaseProduct(userId: string, productId: string) {
  const product = await getProduct(productId);
  const user = await getUser(userId);

  // 決済処理
  await processPayment(user, product.price);

  // 注文履歴への記録
  await createOrder(userId, productId);

  // 問題: 在庫チェックが実装されていない！
}
```

**問題点**: PR説明に明記された「在庫チェック」が実装されていません。これにより在庫がない商品も購入できてしまいます。

### ✅ 良い例

```typescript
async function purchaseProduct(userId: string, productId: string) {
  const product = await getProduct(productId);
  const user = await getUser(userId);

  // 在庫チェック
  if (product.stock <= 0) {
    throw new Error('Product out of stock');
  }

  // 決済処理
  await processPayment(user, product.price);

  // 在庫の減少
  await decrementStock(productId);

  // 注文履歴への記録
  await createOrder(userId, productId);
}
```

**理由**: PR説明に記載されたすべての機能が実装されています。

---

### ❌ 悪い例：ビジネスロジックの誤り

```python
# 仕様: "割引は商品価格の10%だが、最低100円、最大1000円まで"

def calculate_discount(price):
    discount = price * 0.1
    # 問題: 最低金額と最大金額の制約が実装されていない
    return discount
```

**問題点**: 仕様に明記された制約条件が実装されておらず、不正確な割引計算になります。

### ✅ 良い例

```python
def calculate_discount(price):
    discount = price * 0.1
    # 最低100円、最大1000円の制約を適用
    discount = max(100, min(discount, 1000))
    return discount
```

**理由**: 仕様通りに最低・最大金額の制約が実装されています。

---

### ❌ 悪い例：入出力の不一致

```typescript
// API仕様: "レスポンスは { userId, userName, email, createdAt } の形式"

async function getUser(id: string) {
  const user = await db.users.findOne({ id });

  // 問題: createdAt が含まれていない
  return {
    userId: user.id,
    userName: user.name,
    email: user.email
  };
}
```

**問題点**: API仕様で定義された`createdAt`フィールドが欠落しており、クライアント側でエラーになる可能性があります。

### ✅ 良い例

```typescript
async function getUser(id: string) {
  const user = await db.users.findOne({ id });

  return {
    userId: user.id,
    userName: user.name,
    email: user.email,
    createdAt: user.createdAt.toISOString()
  };
}
```

**理由**: API仕様で定義されたすべてのフィールドが含まれています。

---

### ❌ 悪い例：ユーザーストーリーの未達成

```javascript
// ユーザーストーリー: "管理者は全ユーザーの一覧を見ることができる"
// Acceptance Criteria: "ページネーション対応、ユーザー名でフィルタリング可能"

function getUserList() {
  // 問題: ページネーションが実装されていない
  // 問題: フィルタリング機能がない
  return db.users.findAll();
}
```

**問題点**: ユーザーストーリーのAcceptance Criteriaが満たされていません。

### ✅ 良い例

```javascript
function getUserList(page = 1, limit = 20, nameFilter = null) {
  let query = db.users;

  // フィルタリング
  if (nameFilter) {
    query = query.where('name', 'like', `%${nameFilter}%`);
  }

  // ページネーション
  return query
    .skip((page - 1) * limit)
    .limit(limit)
    .exec();
}
```

**理由**: ユーザーストーリーのすべてのAcceptance Criteriaが実装されています。

---

## 関連観点

- [C01] バグ検出
- [T01] テストカバレッジ
- [DOC02] ドキュメント整合性

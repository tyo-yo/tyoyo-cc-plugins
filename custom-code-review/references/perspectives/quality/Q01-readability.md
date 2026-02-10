# 読みやすさ

**ID**: Q01
**カテゴリ**: 品質と保守性
**優先度**: Tier 1（必須）
**信頼度基準**: 80-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [matsengrp/plugins](https://github.com/matsengrp/plugins)

---

## 概要

読みやすさは、コードの理解しやすさを評価します。コードは書かれるよりも読まれる回数の方が圧倒的に多いため、理解しやすいコードは保守性の基盤となります。

明確で説明的な変数名、適切な関数分割、深すぎるネストの回避、マジックナンバーの排除、適切な関数・行の長さなどが重要です。

---

## チェック内容

- 明確で説明的な変数名
  - `x`、`tmp`、`data` → `userName`、`tempFilePath`、`customerData`
  - 省略形を避ける（`usr` → `user`）
  - 意味のある名前（`flag` → `isActive`、`val` → `totalPrice`）
- 適切な関数分割
  - 1つの関数は1つの責任
  - 複雑なロジックは小さな関数に分割
  - 抽象化レベルの統一
- 深すぎるネスト（3階層以上）
  - 早期リターンの使用
  - ガード節の活用
  - 関数抽出
- 複雑な三項演算子の連鎖
  - ネストした三項演算子の回避
  - if-else文への書き換え
- マジックナンバー
  - 定数化（`if (age > 18)` → `if (age > ADULT_AGE)`）
  - 列挙型の使用
- 長すぎる関数（50行以上）
  - 責任の分割
  - ヘルパー関数の抽出
- 長すぎる行（120文字以上）
  - 適切な改行
  - 変数抽出

---

## 適用基準

### 使用する場合

- ✅ 常に適用
- ✅ すべてのコード変更

### 使用しない場合

- ❌ 適用しない場合なし（常に適用）

---

## 具体例

### ❌ 悪い例

```typescript
// 不明確な変数名、深いネスト、マジックナンバー
function p(u: any) {
  if (u) {
    if (u.a > 18) {
      if (u.s === 'active') {
        if (u.b > 1000) {
          return true;
        }
      }
    }
  }
  return false;
}

// 長い関数、複雑な三項演算子
function processOrder(o: any) {
  const t = o.t === 'express' ? o.p * 1.5 : o.t === 'standard' ? o.p : o.p * 0.8;
  const s = o.i > 10 ? 'bulk' : o.i > 5 ? 'medium' : 'small';
  // ... 50行以上のロジック ...
  return { t, s };
}

// マジックナンバー
if (status === 1) {
  // 1は何を意味する?
}
```

**問題点**: 不明確な変数名、深いネスト、マジックナンバー、複雑な三項演算子、長い関数。

### ✅ 良い例

```typescript
// 明確な変数名、早期リターン、定数化
const ADULT_AGE = 18;
const PREMIUM_BALANCE_THRESHOLD = 1000;
const ACTIVE_STATUS = 'active';

function isPremiumActiveAdult(user: User): boolean {
  // ガード節による早期リターン
  if (!user) {
    return false;
  }

  if (user.age <= ADULT_AGE) {
    return false;
  }

  if (user.status !== ACTIVE_STATUS) {
    return false;
  }

  return user.balance > PREMIUM_BALANCE_THRESHOLD;
}

// 関数分割、明確な変数名
enum OrderType {
  Express = 'express',
  Standard = 'standard',
  Economy = 'economy'
}

function calculateShippingFee(order: Order): number {
  switch (order.type) {
    case OrderType.Express:
      return order.basePrice * 1.5;
    case OrderType.Standard:
      return order.basePrice;
    case OrderType.Economy:
      return order.basePrice * 0.8;
    default:
      throw new Error(`Unknown order type: ${order.type}`);
  }
}

function determineOrderSize(itemCount: number): string {
  if (itemCount > 10) {
    return 'bulk';
  }
  if (itemCount > 5) {
    return 'medium';
  }
  return 'small';
}

function processOrder(order: Order): OrderResult {
  const shippingFee = calculateShippingFee(order);
  const orderSize = determineOrderSize(order.itemCount);

  return {
    shippingFee,
    orderSize
  };
}

// 列挙型による定数化
enum OrderStatus {
  Pending = 1,
  Processing = 2,
  Shipped = 3,
  Delivered = 4
}

if (status === OrderStatus.Pending) {
  // 明確な意味
}
```

**理由**: 明確な変数名、ガード節による浅いネスト、定数化、関数分割、列挙型の使用。

---

## 関連観点

- [Q02] 複雑性
- [Q03] コード臭
- [Q05] YAGNIチェック

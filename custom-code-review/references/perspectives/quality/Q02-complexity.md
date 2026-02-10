# 複雑性

**ID**: Q02
**カテゴリ**: 品質と保守性
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)

---

## 概要

複雑性は、循環的複雑度（Cyclomatic Complexity）や認知的複雑度（Cognitive Complexity）を評価します。複雑度が高いコードは、理解、テスト、保守が困難になるため、適切なレベルに保つことが重要です。

一般的に、循環的複雑度が10を超える関数は、分割やリファクタリングが推奨されます。

---

## チェック内容

- 高い循環的複雑度（McCabe > 10）
  - 分岐（if、else if、switch）の数
  - ループ（for、while）の数
  - 論理演算子（&&、||）の数
- 多数の分岐条件
  - 長いif-else if-else連鎖
  - 大きなswitchステートメント
- 深いネストレベル
  - 3階層以上のネスト
  - ループ内のif文
- 長い関数やメソッド
  - 50行以上の関数
  - 複数の責任を持つ関数
- 複雑な条件式
  - 多数の論理演算子を含む条件
  - ネストした条件式
  - 否定と論理演算子の組み合わせ

---

## 適用基準

### 使用する場合

- ✅ 複雑なロジック
- ✅ 長い関数（50行以上）
- ✅ 多数の分岐を含む関数

### 使用しない場合

- ❌ シンプルな関数（10行未満）
- ❌ 単純なゲッター・セッター

---

## 具体例

### ❌ 悪い例

```typescript
// 循環的複雑度が高い（> 10）
function calculateDiscount(
  user: User,
  product: Product,
  quantity: number,
  promoCode: string
): number {
  let discount = 0;

  if (user.isPremium) {
    if (product.category === 'electronics') {
      if (quantity > 10) {
        discount = 0.2;
      } else if (quantity > 5) {
        discount = 0.15;
      } else {
        discount = 0.1;
      }
    } else if (product.category === 'books') {
      if (quantity > 20) {
        discount = 0.25;
      } else if (quantity > 10) {
        discount = 0.2;
      } else {
        discount = 0.15;
      }
    }
  } else {
    if (product.category === 'electronics') {
      if (quantity > 10) {
        discount = 0.1;
      } else if (quantity > 5) {
        discount = 0.05;
      }
    } else if (product.category === 'books') {
      if (quantity > 20) {
        discount = 0.15;
      } else if (quantity > 10) {
        discount = 0.1;
      }
    }
  }

  if (promoCode === 'SUMMER2026') {
    discount += 0.05;
  } else if (promoCode === 'WINTER2026') {
    discount += 0.1;
  } else if (promoCode === 'BLACKFRIDAY') {
    discount += 0.15;
  }

  return discount;
}

// 複雑な条件式
if (
  (user.age > 18 && user.country === 'US' && !user.isBanned) ||
  (user.age > 16 && user.country === 'EU' && user.hasParentalConsent) ||
  (user.isAdmin && !user.isSuspended)
) {
  // ...
}
```

**問題点**: 循環的複雑度が高すぎる（20以上）、深いネスト、複雑な条件式。

### ✅ 良い例

```typescript
// 複雑度を下げるための分割
interface DiscountRule {
  userType: 'premium' | 'regular';
  category: string;
  quantity: number;
  discount: number;
}

const DISCOUNT_RULES: DiscountRule[] = [
  { userType: 'premium', category: 'electronics', quantity: 10, discount: 0.2 },
  { userType: 'premium', category: 'electronics', quantity: 5, discount: 0.15 },
  { userType: 'premium', category: 'electronics', quantity: 0, discount: 0.1 },
  { userType: 'premium', category: 'books', quantity: 20, discount: 0.25 },
  { userType: 'premium', category: 'books', quantity: 10, discount: 0.2 },
  { userType: 'premium', category: 'books', quantity: 0, discount: 0.15 },
  { userType: 'regular', category: 'electronics', quantity: 10, discount: 0.1 },
  { userType: 'regular', category: 'electronics', quantity: 5, discount: 0.05 },
  { userType: 'regular', category: 'books', quantity: 20, discount: 0.15 },
  { userType: 'regular', category: 'books', quantity: 10, discount: 0.1 }
];

const PROMO_CODE_DISCOUNTS: Record<string, number> = {
  SUMMER2026: 0.05,
  WINTER2026: 0.1,
  BLACKFRIDAY: 0.15
};

function calculateDiscount(
  user: User,
  product: Product,
  quantity: number,
  promoCode: string
): number {
  const baseDiscount = calculateBaseDiscount(user, product, quantity);
  const promoDiscount = getPromoCodeDiscount(promoCode);

  return baseDiscount + promoDiscount;
}

function calculateBaseDiscount(
  user: User,
  product: Product,
  quantity: number
): number {
  const userType = user.isPremium ? 'premium' : 'regular';

  // ルールを降順で検索（高い割引量から）
  const rule = DISCOUNT_RULES.find(
    (r) =>
      r.userType === userType &&
      r.category === product.category &&
      quantity >= r.quantity
  );

  return rule?.discount ?? 0;
}

function getPromoCodeDiscount(promoCode: string): number {
  return PROMO_CODE_DISCOUNTS[promoCode] ?? 0;
}

// 複雑な条件式を分割
function canAccessContent(user: User): boolean {
  if (isUSAdult(user)) return true;
  if (isEUMinorWithConsent(user)) return true;
  if (isActiveAdmin(user)) return true;

  return false;
}

function isUSAdult(user: User): boolean {
  return user.age > 18 && user.country === 'US' && !user.isBanned;
}

function isEUMinorWithConsent(user: User): boolean {
  return user.age > 16 && user.country === 'EU' && user.hasParentalConsent;
}

function isActiveAdmin(user: User): boolean {
  return user.isAdmin && !user.isSuspended;
}
```

**理由**: ルールベースの設計で複雑度を削減、条件式を小さな関数に分割、データ駆動アプローチ。

---

## 複雑度の測定

循環的複雑度は以下の公式で計算されます。

```
M = E - N + 2P
```

- E: エッジ数（制御フローの矢印）
- N: ノード数（制御フローの節点）
- P: 連結成分数（通常は1）

簡易計算: `分岐点数 + 1`

一般的な基準:
- **1-10**: シンプル、理解しやすい
- **11-20**: 中程度の複雑さ、リファクタリング検討
- **21-50**: 複雑、テストが困難
- **50+**: テスト不可能、必ずリファクタリング

---

## 関連観点

- [Q01] 読みやすさ
- [Q03] コード臭
- [D01] 型設計とカプセル化

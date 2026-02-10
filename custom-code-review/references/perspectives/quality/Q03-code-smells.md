# コード臭

**ID**: Q03
**カテゴリ**: 品質と保守性
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [matsengrp/plugins](https://github.com/matsengrp/plugins)

---

## 概要

コード臭（Code Smells）は、リファクタリングが必要なコードパターンを検出します。コード臭は必ずしもバグではありませんが、将来的にバグや保守性の問題につながる可能性があるため、早期に対処することが推奨されます。

Martin Fowlerの「リファクタリング」で定義された代表的なコード臭を中心に評価します。

---

## チェック内容

- 重複コード（Duplicated Code）
  - 同じロジックの繰り返し
  - コピー&ペーストコード
  - 類似パターンの複数実装
- 長いメソッド（Long Method）
  - 50行以上の関数
  - 複数の責任を持つ関数
- 大きなクラス（Large Class）
  - 多数のフィールド（10以上）
  - 多数のメソッド（20以上）
  - 複数の責任を持つクラス
- 長いパラメータリスト（Long Parameter List）
  - 4個以上のパラメータ
  - パラメータオブジェクトで置き換え可能
- 特性の横恋慕（Feature Envy）
  - 他のクラスのデータに過度に依存
  - メソッドの移動が必要
- データの群れ（Data Clumps）
  - 常に一緒に現れるデータ
  - オブジェクトにまとめるべき
- プリミティブへの執着（Primitive Obsession）
  - プリミティブ型の過度な使用
  - ドメインオブジェクトで置き換え可能
- Switch文の乱用（Switch Statements）
  - 型コードによる分岐
  - ポリモーフィズムで置き換え可能
- 一時フィールド（Temporary Field）
  - 特定の条件下でのみ使用されるフィールド
  - パラメータに置き換え可能
- メッセージチェーン（Message Chains）
  - `a.getB().getC().getD()`
  - デメテルの法則違反

---

## 適用基準

### 使用する場合

- ✅ 新規実装
- ✅ リファクタリング候補
- ✅ コード追加・変更

### 使用しない場合

- ❌ ドキュメント変更のみ

---

## 具体例

### ❌ 悪い例

```typescript
// 重複コード
function calculatePriceForPremiumUser(price: number): number {
  const discount = price * 0.1;
  const tax = (price - discount) * 0.08;
  return price - discount + tax;
}

function calculatePriceForRegularUser(price: number): number {
  const discount = price * 0.05;
  const tax = (price - discount) * 0.08;
  return price - discount + tax;
}

// 長いパラメータリスト
function createUser(
  name: string,
  email: string,
  age: number,
  country: string,
  city: string,
  zipCode: string,
  phoneNumber: string
): User {
  // ...
}

// データの群れ
function sendEmail(
  recipientName: string,
  recipientEmail: string,
  recipientPhone: string,
  senderName: string,
  senderEmail: string,
  senderPhone: string
): void {
  // ...
}

// プリミティブへの執着
function processOrder(
  orderType: string, // "express", "standard", "economy"
  paymentMethod: string, // "credit", "debit", "paypal"
  status: number // 1: pending, 2: processing, 3: shipped
): void {
  // ...
}

// メッセージチェーン
const userName = order.getCustomer().getAccount().getProfile().getName();
```

**問題点**: 重複コード、長いパラメータリスト、データの群れ、プリミティブへの執着、メッセージチェーン。

### ✅ 良い例

```typescript
// 重複コードの解消（共通ロジック抽出）
function calculatePrice(price: number, discountRate: number): number {
  const discount = price * discountRate;
  const tax = (price - discount) * 0.08;
  return price - discount + tax;
}

function calculatePriceForPremiumUser(price: number): number {
  return calculatePrice(price, 0.1);
}

function calculatePriceForRegularUser(price: number): number {
  return calculatePrice(price, 0.05);
}

// パラメータオブジェクトで長いパラメータリスト解消
interface UserInput {
  name: string;
  email: string;
  age: number;
  address: Address;
  phoneNumber: string;
}

interface Address {
  country: string;
  city: string;
  zipCode: string;
}

function createUser(input: UserInput): User {
  // ...
}

// データの群れをオブジェクトに
interface Contact {
  name: string;
  email: string;
  phone: string;
}

function sendEmail(recipient: Contact, sender: Contact): void {
  // ...
}

// プリミティブへの執着を解消（ドメインオブジェクト使用）
enum OrderType {
  Express = 'express',
  Standard = 'standard',
  Economy = 'economy'
}

enum PaymentMethod {
  Credit = 'credit',
  Debit = 'debit',
  PayPal = 'paypal'
}

enum OrderStatus {
  Pending = 1,
  Processing = 2,
  Shipped = 3
}

function processOrder(
  orderType: OrderType,
  paymentMethod: PaymentMethod,
  status: OrderStatus
): void {
  // ...
}

// メッセージチェーンを解消（デメテルの法則）
// 悪い例: order.getCustomer().getAccount().getProfile().getName()
class Order {
  getCustomerName(): string {
    return this.customer.getAccountName();
  }
}

class Customer {
  getAccountName(): string {
    return this.account.getProfileName();
  }
}

class Account {
  getProfileName(): string {
    return this.profile.name;
  }
}

// 使用側
const userName = order.getCustomerName();
```

**理由**: 共通ロジック抽出、パラメータオブジェクト、ドメインオブジェクト、デメテルの法則遵守。

---

## 教育的出力フォーマット

コード臭検出時は、教育的な出力を提供します。

```markdown
**Code Smell**: [臭いの種類]
- **What**: [問題の説明]
- **Why it matters**: [なぜ問題か]
- **Location**: [ファイルパス:行番号]
- **How to fix**: [修正方法]
- **Learn more**: [参考資料]
- **Confidence**: [スコア]
```

例:

```markdown
**Code Smell**: Data Clumps
- **What**: `recipientName`, `recipientEmail`, `recipientPhone` が常に一緒に現れています
- **Why it matters**: データが分散していると、変更時に複数箇所を修正する必要があり、一貫性が損なわれます
- **Location**: src/email.ts:15
- **How to fix**: `Contact` インターフェースにまとめて、`sendEmail(recipient: Contact, sender: Contact)` とする
- **Learn more**: [Refactoring: Data Clumps](https://refactoring.guru/smells/data-clumps)
- **Confidence**: 90
```

---

## 関連観点

- [Q01] 読みやすさ
- [Q02] 複雑性
- [Q04] アンチパターン
- [Q05] YAGNIチェック

# データフロー設計

**ID**: D05
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 3（オプション）
**信頼度基準**: 80-100点

---

## 参照元

- [Feature Dev - code-explorer, code-architect](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

データフロー設計は、システム内でのデータの流れ、変換、状態変化を明確にする設計活動です。適切なデータフロー設計により、バグの早期発見、デバッグの容易化、保守性の向上が期待できます。本観点では、データ変換の明確性、状態変化の追跡可能性、副作用の明示性、データの不変性を評価します。

---

## チェック内容

- データ変換の明確性
  - 入力から出力までの変換ステップが明確
  - 各ステップでのデータ形式が型で表現されている
  - 変換ロジックがテスト可能
- 状態変化の追跡可能性
  - 状態遷移が明示的
  - 状態変更のログ記録
  - イベント駆動での状態管理
- 副作用の明示性
  - 純粋関数と副作用のある関数の分離
  - 副作用の範囲が限定的
  - 副作用の発生箇所が明確
- データの不変性
  - 不変データ構造の使用
  - 変更時には新しいオブジェクトを生成
  - 共有状態の最小化

---

## 適用基準

### 使用する場合

- ✅ データ変換ロジック追加
- ✅ 状態管理変更
- ✅ ストリーム処理実装
- ✅ イベント駆動アーキテクチャ
- ✅ リアクティブプログラミング

### 使用しない場合

- ❌ 単純なCRUD操作のみ
- ❌ ステートレスな処理
- ❌ ドキュメント変更のみ

---

## 具体例

### ❌ 悪い例: データ変換が不明確

```javascript
function processUserData(data) {
  // 何が起こっているか不明確
  data.name = data.firstName + ' ' + data.lastName;
  data.age = new Date().getFullYear() - data.birthYear;
  data.email = data.email.toLowerCase();
  delete data.firstName;
  delete data.lastName;
  delete data.birthYear;
  if (data.age < 18) {
    data.status = 'minor';
  } else {
    data.status = 'adult';
  }
  return data;
}
```

**問題点**: データの変換が1つの関数内で混在し、変換ステップが不明確です。また、元のデータを破壊的に変更しています。

### ✅ 良い例: 明確なデータ変換パイプライン

```javascript
// 型定義で各ステップのデータ形式を明確化
interface RawUserData {
  firstName: string;
  lastName: string;
  birthYear: number;
  email: string;
}

interface NormalizedUserData {
  fullName: string;
  age: number;
  email: string;
}

interface EnrichedUserData extends NormalizedUserData {
  status: 'minor' | 'adult';
}

// ステップ1: 名前の結合
function combineNames(data: RawUserData): Omit<RawUserData, 'firstName' | 'lastName'> & { fullName: string } {
  return {
    fullName: `${data.firstName} ${data.lastName}`,
    birthYear: data.birthYear,
    email: data.email,
  };
}

// ステップ2: 年齢計算
function calculateAge(data: ReturnType<typeof combineNames>): NormalizedUserData {
  return {
    fullName: data.fullName,
    age: new Date().getFullYear() - data.birthYear,
    email: data.email.toLowerCase(),
  };
}

// ステップ3: ステータス付与
function enrichStatus(data: NormalizedUserData): EnrichedUserData {
  return {
    ...data,
    status: data.age < 18 ? 'minor' : 'adult',
  };
}

// パイプライン（不変性を保持）
function processUserData(rawData: RawUserData): EnrichedUserData {
  return pipe(
    rawData,
    combineNames,
    calculateAge,
    enrichStatus
  );
}

// ユーティリティ関数
function pipe<T>(value: T, ...fns: Array<(arg: any) => any>) {
  return fns.reduce((acc, fn) => fn(acc), value);
}
```

**理由**: 各変換ステップが明確で、型による保証があり、不変性を保持しています。

---

### ❌ 悪い例: 状態変化が追跡困難

```python
class Order:
    def __init__(self, items):
        self.items = items
        self.status = 'pending'
        self.total = 0

    def process(self):
        # 状態変化が暗黙的
        self.status = 'processing'
        self.total = sum(item.price for item in self.items)
        # 支払い処理（副作用）
        payment.charge(self.total)
        # さらに状態変化
        self.status = 'paid'
        # メール送信（副作用）
        email.send(self.user, 'Order confirmed')
        self.status = 'completed'
```

**問題点**: 状態変化が暗黙的で、副作用が散在しています。エラー発生時にどの状態にあるか不明です。

### ✅ 良い例: 明示的な状態遷移

```python
from enum import Enum
from typing import List
from dataclasses import dataclass
import logging

class OrderStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    PAYMENT_PENDING = 'payment_pending'
    PAID = 'paid'
    COMPLETED = 'completed'
    FAILED = 'failed'

@dataclass(frozen=True)  # 不変
class Order:
    id: str
    items: List[Item]
    status: OrderStatus
    total: float

class OrderService:
    def __init__(self, payment_service, email_service, logger):
        self.payment = payment_service
        self.email = email_service
        self.logger = logger

    def process_order(self, order: Order) -> Order:
        # ステップ1: 処理開始
        order = self._transition(order, OrderStatus.PROCESSING)

        try:
            # ステップ2: 合計計算
            total = sum(item.price for item in order.items)
            order = self._update_total(order, total)

            # ステップ3: 支払い処理
            order = self._transition(order, OrderStatus.PAYMENT_PENDING)
            self.payment.charge(order.total)
            order = self._transition(order, OrderStatus.PAID)

            # ステップ4: 通知送信
            self.email.send(order.user, 'Order confirmed')
            order = self._transition(order, OrderStatus.COMPLETED)

            return order
        except Exception as e:
            self.logger.error(f"Order processing failed: {e}")
            return self._transition(order, OrderStatus.FAILED)

    def _transition(self, order: Order, new_status: OrderStatus) -> Order:
        self.logger.info(f"Order {order.id}: {order.status.value} -> {new_status.value}")
        return Order(order.id, order.items, new_status, order.total)

    def _update_total(self, order: Order, total: float) -> Order:
        return Order(order.id, order.items, order.status, total)
```

**理由**: 状態遷移が明示的でログに記録され、不変データ構造により各ステップが追跡可能です。

---

### ❌ 悪い例: 副作用が混在

```javascript
function calculateDiscount(user, order) {
  // 純粋な計算と副作用が混在
  let discount = 0;

  if (user.isPremium) {
    discount = order.total * 0.1;
    // 副作用: データベース更新
    db.updateUserStats(user.id, { discountsUsed: user.discountsUsed + 1 });
  }

  // 副作用: ログ記録
  logger.info(`Discount calculated: ${discount}`);

  return discount;
}
```

**問題点**: 割引計算（純粋関数）とデータベース更新・ログ記録（副作用）が混在しています。

### ✅ 良い例: 純粋関数と副作用の分離

```javascript
// 純粋関数: 副作用なし、同じ入力に対して同じ出力
function calculateDiscount(isPremium: boolean, total: number): number {
  return isPremium ? total * 0.1 : 0;
}

// 副作用を持つ関数（明示的）
async function applyDiscount(user: User, order: Order): Promise<DiscountResult> {
  // 純粋関数を呼び出し
  const discount = calculateDiscount(user.isPremium, order.total);

  // 副作用を明示的に実行
  if (discount > 0) {
    await db.updateUserStats(user.id, {
      discountsUsed: user.discountsUsed + 1
    });
    logger.info(`Discount applied for user ${user.id}: ${discount}`);
  }

  return {
    discount,
    finalTotal: order.total - discount
  };
}
```

**理由**: 純粋関数（テスト容易）と副作用のある関数を分離し、それぞれの責務が明確です。

---

### ❌ 悪い例: 共有可変状態

```typescript
// グローバルな可変状態
let currentUser: User | null = null;

function login(username: string, password: string) {
  const user = authenticate(username, password);
  currentUser = user;  // 共有状態を変更
}

function updateProfile(data: any) {
  if (currentUser) {
    currentUser.name = data.name;  // 可変状態を変更
    currentUser.email = data.email;
  }
}

function logout() {
  currentUser = null;  // 共有状態を変更
}
```

**問題点**: グローバルな可変状態により、どこからでも状態を変更でき、バグの原因となります。

### ✅ 良い例: 不変データと明示的な状態管理

```typescript
// 不変データ構造
interface User {
  readonly id: string;
  readonly name: string;
  readonly email: string;
}

// 状態管理を専用のクラスに集約
class UserSession {
  private currentUser: User | null = null;

  login(username: string, password: string): User {
    const user = authenticate(username, password);
    this.currentUser = user;
    return user;
  }

  updateProfile(data: Partial<User>): User {
    if (!this.currentUser) {
      throw new Error('No user logged in');
    }

    // 新しいオブジェクトを作成（不変性）
    this.currentUser = {
      ...this.currentUser,
      ...data
    };

    return this.currentUser;
  }

  logout(): void {
    this.currentUser = null;
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }
}

// 使用例
const session = new UserSession();
```

**理由**: 状態管理を専用のクラスに集約し、不変データ構造により予期しない変更を防ぎます。

---

## 2026年トレンド

データフロー設計において以下のトレンドが見られます。

- 関数型プログラミングパラダイムの普及（不変性、純粋関数）
- リアクティブプログラミング（RxJS、Redux、Vuex）
- イベントソーシング（Event Sourcing）とCQRS
- ストリーム処理（Apache Kafka、AWS Kinesis）
- 型システムによるデータフロー保証（TypeScriptの型推論）

AI生成コードは、副作用を適切に分離せず、可変状態を多用する傾向があるため、データフローレビューが重要です。

---

## 関連観点

- [D01] 型設計とカプセル化
- [C01] バグ検出
- [Q01] 読みやすさ
- [D02] アーキテクチャパターン準拠

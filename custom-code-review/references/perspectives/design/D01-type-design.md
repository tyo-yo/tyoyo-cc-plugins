# 型設計とカプセル化

**ID**: D01
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [PR Review Toolkit - type-design-analyzer](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

型設計は、型システムを活用してビジネスルールや制約をコンパイル時に強制する設計手法です。適切な型設計により、実行時エラーを防ぎ、コードの自己説明性を高めます。本観点では、型の不変性（invariants）、カプセル化、型安全性を評価し、より堅牢な型設計を提案します。

---

## チェック内容

- 不変性（Invariants）の識別
  - ビジネスルールの型による表現
  - 無効な状態の構築不可能性
  - 型による前提条件の明示
- カプセル化の評価
  - 内部実装の隠蔽度
  - 外部からの違反可能性
  - アクセス修飾子の適切性
  - 不変性の保護
- 型安全性の評価
  - コンパイル時エラー検出
  - 型による自己説明性
  - プリミティブ型の適切な使用
  - 型エイリアスとニュータイプ
- Pydanticデータクラス（Python）
  - バリデーションロジックの適切性
  - フィールドの型安全性
  - デフォルト値の妥当性

---

## 適用基準

### 使用する場合

- ✅ 新しい型・クラス追加
- ✅ データモデルの設計
- ✅ 型安全言語（TypeScript、Java、C#、Rust、Go、Python with Pydantic）
- ✅ APIレスポンス/リクエストの型定義

### 使用しない場合

- ❌ 動的型付け言語での単純なスクリプト
- ❌ プロトタイプコード
- ❌ 型定義を含まない変更

---

## 具体例

### ❌ 悪い例: プリミティブ型の乱用

```typescript
function createUser(
  name: string,
  email: string,
  age: number,
  status: string
): User {
  // statusは "active" | "inactive" | "banned" のみ許可されるべき
  // ageは正の整数のみ許可されるべき
  return { name, email, age, status };
}

// 誤った使用が可能
createUser("Alice", "invalid-email", -5, "unknown");
```

**問題点**: プリミティブ型を使用しているため、無効な値の受け渡しが可能です。

### ✅ 良い例: 型による制約の表現

```typescript
type Email = string & { readonly __brand: unique symbol };
type PositiveInt = number & { readonly __brand: unique symbol };
type UserStatus = "active" | "inactive" | "banned";

interface User {
  name: string;
  email: Email;
  age: PositiveInt;
  status: UserStatus;
}

function createEmail(value: string): Email {
  if (!value.includes('@')) {
    throw new Error('Invalid email');
  }
  return value as Email;
}

function createPositiveInt(value: number): PositiveInt {
  if (value <= 0 || !Number.isInteger(value)) {
    throw new Error('Must be positive integer');
  }
  return value as PositiveInt;
}

function createUser(
  name: string,
  email: Email,
  age: PositiveInt,
  status: UserStatus
): User {
  return { name, email, age, status };
}

// 型安全な使用
const email = createEmail("alice@example.com");
const age = createPositiveInt(25);
createUser("Alice", email, age, "active");
```

**理由**: 型によってビジネスルールを表現し、無効な値の受け渡しをコンパイル時に防ぎます。

---

### ❌ 悪い例: カプセル化の欠如

```python
class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance  # publicフィールド

    def withdraw(self, amount: float):
        self.balance -= amount  # 残高チェックなし

# 不正な操作が可能
account = BankAccount(100)
account.balance = -500  # 直接変更可能
account.withdraw(200)    # 残高がマイナスになる
```

**問題点**: `balance`が外部から直接変更可能で、不変性（残高は負にならない）が保証されていません。

### ✅ 良い例: カプセル化による不変性の保護

```python
class BankAccount:
    def __init__(self, balance: float):
        if balance < 0:
            raise ValueError("Initial balance must be non-negative")
        self._balance = balance  # privateフィールド

    @property
    def balance(self) -> float:
        return self._balance

    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance < amount:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
```

**理由**: 内部状態をprivateにし、不変性（残高は負にならない）を保護しています。

---

### ❌ 悪い例: 無効な状態の構築可能性

```rust
struct Order {
    id: String,
    status: String,
    items: Vec<Item>,
    total: f64,
}

// 無効な状態が構築可能
let order = Order {
    id: "".to_string(),        // 空のID
    status: "unknown".to_string(), // 不正なステータス
    items: vec![],              // 空の商品リスト
    total: -100.0,              // 負の合計金額
};
```

**問題点**: 無効な状態のOrderが構築可能です。

### ✅ 良い例: 型による無効状態の防止

```rust
use std::num::NonZeroU64;

enum OrderStatus {
    Pending,
    Confirmed,
    Shipped,
    Delivered,
}

struct OrderId(NonZeroU64);

struct Order {
    id: OrderId,
    status: OrderStatus,
    items: Vec<Item>,
    total: f64,
}

impl Order {
    fn new(id: NonZeroU64, items: Vec<Item>) -> Result<Self, String> {
        if items.is_empty() {
            return Err("Order must have at least one item".to_string());
        }

        let total: f64 = items.iter().map(|item| item.price).sum();
        if total <= 0.0 {
            return Err("Order total must be positive".to_string());
        }

        Ok(Order {
            id: OrderId(id),
            status: OrderStatus::Pending,
            items,
            total,
        })
    }
}
```

**理由**: コンストラクタで制約をチェックし、列挙型とニュータイプを使用して無効な状態を防ぎます。

---

### ❌ 悪い例: Pydanticバリデーション不足

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    age: int

# 無効な値が許容される
user = UserCreate(username="", password="123", age=-5)
```

**問題点**: バリデーションが不足しており、無効な値が許容されます。

### ✅ 良い例: 適切なPydanticバリデーション

```python
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=0, le=150)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v

    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        return v
```

**理由**: Fieldバリデーションとカスタムバリデーターを使用して、ビジネスルールを強制しています。

---

## 2026年トレンド

型安全性への関心が高まり、以下の傾向が見られます。

- TypeScriptでのBranded Type（ニュータイプ）の活用
- Pythonでの型ヒント（Type Hints）とPydanticの普及
- Rustの所有権システムに影響を受けた設計パターン
- 「Parse, don't validate」哲学（パースに成功した時点で型保証）

AIコード生成は、プリミティブ型を多用する傾向があるため、適切な型設計が特に重要です。

---

## 関連観点

- [C01] バグ検出
- [C05] 例外安全性
- [D02] アーキテクチャパターン準拠
- [Q01] 読みやすさ

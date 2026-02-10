# 依存関係管理

**ID**: D04
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [Feature Dev - code-explorer](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

依存関係管理は、モジュール間、コンポーネント間、ライブラリ間の依存を適切に管理する設計活動です。適切な依存関係管理により、保守性、テスタビリティ、再利用性が向上します。本観点では、循環依存、依存関係の最小化、適切な抽象化レベルを評価します。なお、セキュリティ脆弱性のある外部ライブラリの検出はDependabotなどのツールで対応するため、ここでは設計上の依存関係を対象とします。

---

## チェック内容

- 循環依存の回避（ツールで検出不可のもの）
  - モジュール間の循環依存
  - クラス間の循環依存
  - パッケージ間の循環依存
- 依存関係の最小化
  - 不要な依存の削除
  - 依存の正当性確認
  - 推移的依存の最小化
- 適切な抽象化レベル
  - 上位層から下位層への依存（依存関係逆転の原則）
  - インターフェースへの依存
  - 具象クラスへの直接依存の回避
- 依存性注入（DI）の適切な使用
  - コンストラクタインジェクション
  - テスタビリティの向上
  - 疎結合の実現

---

## 適用基準

### 使用する場合

- ✅ 依存関係追加・変更
- ✅ ライブラリアップグレード
- ✅ 新規モジュール追加
- ✅ アーキテクチャ変更

### 使用しない場合

- ❌ 単一ファイル内の変更
- ❌ テストコードのみの変更
- ❌ ドキュメントのみの変更

---

## 具体例

### ❌ 悪い例: 循環依存

```python
# user.py
from order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def place_order(self, items):
        order = Order(self, items)
        self.orders.append(order)
        return order

# order.py
from user import User  # 循環依存

class Order:
    def __init__(self, user: User, items):
        self.user = user
        self.items = items

    def get_user_name(self):
        return self.user.name
```

**問題点**: `user.py`と`order.py`が相互にインポートし、循環依存が発生しています。

### ✅ 良い例: 依存関係の整理

```python
# user.py
class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

# order.py
class Order:
    def __init__(self, user_id: str, user_name: str, items):
        self.user_id = user_id
        self.user_name = user_name
        self.items = items

# order_service.py（オーケストレーション層）
from user import User
from order import Order

class OrderService:
    def place_order(self, user: User, items):
        order = Order(user.id, user.name, items)
        user.add_order(order)
        return order
```

**理由**: 循環依存を解消し、オーケストレーション層で依存を管理しています。

---

### ❌ 悪い例: 不要な依存

```javascript
// utils.js
import axios from 'axios';          // HTTP通信に使用
import lodash from 'lodash';        // 配列操作に使用
import moment from 'moment';        // 日付操作に使用
import validator from 'validator';  // バリデーションに使用
import crypto from 'crypto';        // 暗号化に使用

// 実際には lodash の sum 関数のみ使用
export function calculateTotal(prices) {
  return lodash.sum(prices);
}
```

**問題点**: `lodash`の`sum`関数のみ使用するのに、多数の不要な依存をインポートしています。

### ✅ 良い例: 依存の最小化

```javascript
// utils.js
// ネイティブのreduce関数で代替
export function calculateTotal(prices) {
  return prices.reduce((sum, price) => sum + price, 0);
}

// もしくは必要な関数のみインポート
import { sum } from 'lodash/sum';

export function calculateTotal(prices) {
  return sum(prices);
}
```

**理由**: ネイティブ機能で代替するか、必要な関数のみをインポートしています。

---

### ❌ 悪い例: 具象クラスへの直接依存

```java
public class OrderProcessor {
    private MySQLDatabase database;
    private SmtpEmailService emailService;
    private StripePaymentGateway paymentGateway;

    public OrderProcessor() {
        // 具象クラスに直接依存
        this.database = new MySQLDatabase("localhost", 3306);
        this.emailService = new SmtpEmailService("smtp.example.com");
        this.paymentGateway = new StripePaymentGateway("api_key");
    }

    public void processOrder(Order order) {
        paymentGateway.charge(order.getTotal());
        database.save(order);
        emailService.send(order.getUserEmail(), "Order confirmed");
    }
}
```

**問題点**: 具象クラスに直接依存しており、テストやデータベース/メール/決済サービスの切り替えが困難です。

### ✅ 良い例: インターフェースへの依存と依存性注入

```java
// インターフェース定義
public interface Database {
    void save(Order order);
}

public interface EmailService {
    void send(String to, String subject, String body);
}

public interface PaymentGateway {
    void charge(BigDecimal amount);
}

// 実装
public class OrderProcessor {
    private final Database database;
    private final EmailService emailService;
    private final PaymentGateway paymentGateway;

    // 依存性注入（コンストラクタインジェクション）
    public OrderProcessor(
        Database database,
        EmailService emailService,
        PaymentGateway paymentGateway
    ) {
        this.database = database;
        this.emailService = emailService;
        this.paymentGateway = paymentGateway;
    }

    public void processOrder(Order order) {
        paymentGateway.charge(order.getTotal());
        database.save(order);
        emailService.send(
            order.getUserEmail(),
            "Order confirmed",
            "Your order has been processed."
        );
    }
}

// 使用例
Database db = new MySQLDatabase("localhost", 3306);
EmailService email = new SmtpEmailService("smtp.example.com");
PaymentGateway payment = new StripePaymentGateway("api_key");

OrderProcessor processor = new OrderProcessor(db, email, payment);
```

**理由**: インターフェースへの依存により、実装の切り替えが容易になり、テスタビリティが向上します。

---

### ❌ 悪い例: レイヤー逆転（下位層が上位層に依存）

```typescript
// データアクセス層
class UserRepository {
  async findById(id: string): Promise<User> {
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);

    // ビジネスロジック層のバリデーションを直接呼び出し（逆転）
    if (!UserValidator.isActive(result)) {
      throw new Error('User is not active');
    }

    return new User(result);
  }
}

// ビジネスロジック層
class UserValidator {
  static isActive(user: any): boolean {
    return user.status === 'active';
  }
}
```

**問題点**: データアクセス層がビジネスロジック層に依存し、依存関係が逆転しています。

### ✅ 良い例: 適切な依存の方向性

```typescript
// データアクセス層（下位層）
class UserRepository {
  async findById(id: string): Promise<User | null> {
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result ? new User(result) : null;
  }
}

// ビジネスロジック層（上位層）
class UserService {
  constructor(private repository: UserRepository) {}

  async getActiveUser(id: string): Promise<User> {
    const user = await this.repository.findById(id);

    if (!user) {
      throw new Error('User not found');
    }

    if (!this.isActive(user)) {
      throw new Error('User is not active');
    }

    return user;
  }

  private isActive(user: User): boolean {
    return user.status === 'active';
  }
}
```

**理由**: 上位層（ビジネスロジック）から下位層（データアクセス）への単方向依存を維持しています。

---

### ❌ 悪い例: 推移的依存の増大

```json
// package.json
{
  "dependencies": {
    "express": "^4.18.0",
    "body-parser": "^1.20.0",  // express に含まれている（不要）
    "compression": "^1.7.4",   // express に含まれている（不要）
    "morgan": "^1.10.0",       // ログ用
    "winston": "^3.8.0",       // ログ用（morganと重複）
    "pino": "^8.11.0"          // ログ用（morganと重複）
  }
}
```

**問題点**: 重複した機能の依存が複数含まれ、推移的依存が増大しています。

### ✅ 良い例: 依存の整理

```json
// package.json
{
  "dependencies": {
    "express": "^4.18.0",     // body-parser, compressionを含む
    "winston": "^3.8.0"       // 統一したログライブラリ
  }
}
```

**理由**: 重複を排除し、必要最小限の依存に整理しています。

---

## 2026年トレンド

依存関係管理において以下のトレンドが見られます。

- モノレポ（Monorepo）による依存管理の一元化
- パッケージマネージャーのワークスペース機能（npm workspaces、pnpm、Yarn）
- 依存関係の可視化ツール（dependency-cruiser、madge）
- Tree Shakingによる不要コードの削除
- ES Modulesの普及による循環依存の検出容易化

AI生成コードは、既存の依存関係を理解せずに新しい依存を追加する傾向があるため、依存関係レビューが重要です。

---

## 関連観点

- [D02] アーキテクチャパターン準拠
- [Q04] アンチパターン
- [D01] 型設計とカプセル化
- [PERF03] リソース管理

# アーキテクチャパターン準拠

**ID**: D02
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [Feature Dev - code-architect](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [matsengrp/plugins - antipattern-scanner](https://github.com/matsengrp/plugins)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

アーキテクチャパターンは、システム全体の構造を決定する設計パターンです。既存のアーキテクチャパターンへの準拠は、コードベース全体の一貫性、保守性、拡張性を確保するために重要です。本観点では、レイヤー構造、デザインパターン（GOF等）、コンポーネント間のインターフェース、依存関係の方向性を評価します。

---

## チェック内容

- レイヤー構造の遵守
  - プレゼンテーション層 → ビジネスロジック層 → データアクセス層
  - 依存関係の方向性（上位層から下位層への単方向）
  - レイヤー間のインターフェース明確性
- デザインパターンの適切な使用
  - GOFパターン（Singleton、Factory、Strategy、Observer等）
  - アプリケーションアーキテクチャパターン（MVC、MVVM、Clean Architecture等）
  - パターンの過剰適用の回避
- 横断的関心事の分離
  - 認証・認可
  - ログ
  - キャッシング
  - エラーハンドリング
- コンポーネント間のインターフェース
  - 疎結合の維持
  - 明確な責務の境界
  - 依存性注入（DI）の適切な使用

---

## 適用基準

### 使用する場合

- ✅ アーキテクチャ変更
- ✅ 新規コンポーネント追加
- ✅ レイヤー間のインターフェース変更
- ✅ 大規模な機能追加

### 使用しない場合

- ❌ 単一ファイル内の小規模バグ修正
- ❌ ドキュメント変更のみ
- ❌ テストコードのみの変更
- ❌ スタイルのみの変更

---

## 具体例

### ❌ 悪い例: レイヤー境界の違反

```javascript
// プレゼンテーション層（Controller）
class UserController {
  async createUser(req, res) {
    // ビジネスロジック層をスキップして直接データ層にアクセス
    const db = new Database();
    const result = await db.query(
      'INSERT INTO users (name, email) VALUES (?, ?)',
      [req.body.name, req.body.email]
    );

    // ビジネスルールの検証もControllerで実施
    if (!req.body.email.includes('@')) {
      return res.status(400).json({ error: 'Invalid email' });
    }

    res.json({ id: result.insertId });
  }
}
```

**問題点**: Controllerがビジネスロジックとデータアクセスロジックを直接実装し、レイヤー境界を破壊しています。

### ✅ 良い例: 適切なレイヤー分離

```javascript
// プレゼンテーション層（Controller）
class UserController {
  constructor(userService) {
    this.userService = userService;
  }

  async createUser(req, res) {
    try {
      const user = await this.userService.createUser(req.body);
      res.json(user);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }
}

// ビジネスロジック層（Service）
class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async createUser(data) {
    // ビジネスルールの検証
    if (!data.email.includes('@')) {
      throw new Error('Invalid email');
    }

    return await this.userRepository.create(data);
  }
}

// データアクセス層（Repository）
class UserRepository {
  constructor(db) {
    this.db = db;
  }

  async create(data) {
    const result = await this.db.query(
      'INSERT INTO users (name, email) VALUES (?, ?)',
      [data.name, data.email]
    );
    return { id: result.insertId, ...data };
  }
}
```

**理由**: 各層が明確な責務を持ち、依存関係が単方向になっています。

---

### ❌ 悪い例: デザインパターンの過剰適用

```typescript
// 単純なユーザーデータ取得に複数のデザインパターンを適用
interface UserFactory {
  createUser(data: any): User;
}

class DefaultUserFactory implements UserFactory {
  createUser(data: any): User {
    return new User(data);
  }
}

interface UserRepository {
  findById(id: string): User;
}

class UserRepositoryFactory {
  static create(): UserRepository {
    return new DatabaseUserRepository();
  }
}

class UserServiceProxy {
  private realService: UserService;

  constructor() {
    const factory = new DefaultUserFactory();
    const repo = UserRepositoryFactory.create();
    this.realService = new UserService(repo, factory);
  }

  getUser(id: string): User {
    console.log('Proxy: calling real service');
    return this.realService.getUser(id);
  }
}
```

**問題点**: 単純なCRUD操作に対して、Factory、Proxy、Strategyパターンを過剰に適用しています。

### ✅ 良い例: シンプルで適切な設計

```typescript
class UserRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User> {
    const result = await this.db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result ? new User(result) : null;
  }
}

class UserService {
  constructor(private repository: UserRepository) {}

  async getUser(id: string): Promise<User> {
    return await this.repository.findById(id);
  }
}
```

**理由**: 実際の要件に対してシンプルな設計で十分です。デザインパターンは必要になった時点で導入します。

---

### ❌ 悪い例: 横断的関心事の散在

```python
def create_order(user_id, items):
    # 認証チェックが各関数に散在
    if not check_user_authenticated(user_id):
        raise AuthError("Not authenticated")

    # ログが各関数に散在
    logger.info(f"Creating order for user {user_id}")

    try:
        order = Order(user_id, items)
        db.save(order)

        # ログが各関数に散在
        logger.info(f"Order {order.id} created")
        return order
    except Exception as e:
        # エラーハンドリングが各関数に散在
        logger.error(f"Failed to create order: {e}")
        raise

def update_order(order_id, data):
    # 認証チェックが重複
    if not check_user_authenticated(data['user_id']):
        raise AuthError("Not authenticated")

    # ログが重複
    logger.info(f"Updating order {order_id}")

    # ... 同様の処理
```

**問題点**: 認証、ログ、エラーハンドリングが各関数に散在し、重複しています。

### ✅ 良い例: デコレーターによる横断的関心事の分離

```python
from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id')
        if not check_user_authenticated(user_id):
            raise AuthError("Not authenticated")
        return func(*args, **kwargs)
    return wrapper

def log_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Failed {func.__name__}: {e}")
            raise
    return wrapper

@authenticate
@log_operation
def create_order(user_id, items):
    order = Order(user_id, items)
    db.save(order)
    return order

@authenticate
@log_operation
def update_order(order_id, data, user_id):
    order = db.find(order_id)
    order.update(data)
    db.save(order)
    return order
```

**理由**: デコレーターを使用して横断的関心事を分離し、ビジネスロジックに集中できます。

---

### ❌ 悪い例: 密結合

```java
public class OrderService {
    private MySQLDatabase database;
    private SmtpEmailService emailService;

    public OrderService() {
        // 具象クラスに直接依存
        this.database = new MySQLDatabase();
        this.emailService = new SmtpEmailService();
    }

    public void createOrder(Order order) {
        database.save(order);
        emailService.sendConfirmation(order);
    }
}
```

**問題点**: 具象クラスに直接依存しており、テストやデータベース切り替えが困難です。

### ✅ 良い例: 依存性注入による疎結合

```java
public interface Database {
    void save(Order order);
}

public interface EmailService {
    void sendConfirmation(Order order);
}

public class OrderService {
    private final Database database;
    private final EmailService emailService;

    // 依存性注入（コンストラクタインジェクション)
    public OrderService(Database database, EmailService emailService) {
        this.database = database;
        this.emailService = emailService;
    }

    public void createOrder(Order order) {
        database.save(order);
        emailService.sendConfirmation(order);
    }
}
```

**理由**: インターフェースに依存することで、実装の切り替えが容易になり、テスタビリティが向上します。

---

## 2026年トレンド

アーキテクチャパターンの選択において、以下のトレンドが見られます。

- Clean Architecture、Hexagonal Architecture（ポート＆アダプター）の普及
- マイクロサービスアーキテクチャにおけるドメイン駆動設計（DDD）
- イベント駆動アーキテクチャ（Event Sourcing、CQRS）の増加
- 関数型プログラミングパラダイムの影響（不変性、純粋関数）

AI生成コードは、レイヤー境界を無視して「動くコード」を生成する傾向があるため、アーキテクチャレビューが特に重要です。

---

## 関連観点

- [P02] 既存パターンとの整合性
- [D04] 依存関係管理
- [Q04] アンチパターン
- [D01] 型設計とカプセル化

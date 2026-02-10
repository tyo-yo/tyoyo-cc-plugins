# API設計

**ID**: D03
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 3（オプション）
**信頼度基準**: 80-100点

---

## 参照元

- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)
- [8 Best AI Code Review Tools That Catch Real Bugs in 2026](https://www.qodo.ai/blog/best-ai-code-review-tools-2026/)

---

## 概要

API設計は、システム間、モジュール間、ライブラリのインターフェースを定義する重要な設計活動です。適切なAPI設計により、使いやすさ、一貫性、後方互換性を確保できます。本観点では、REST API、GraphQL API、ライブラリAPI（Python SDK、TypeScript Library等）の設計品質を評価します。

---

## チェック内容

- RESTful原則の遵守（該当する場合）
  - 適切なHTTPメソッドの使用（GET、POST、PUT、PATCH、DELETE）
  - リソース指向のURL設計
  - ステートレス性
  - 適切なHTTPステータスコードの返却
- API命名の一貫性
  - エンドポイント名の統一（複数形 vs 単数形）
  - パラメータ命名規則の統一（camelCase vs snake_case）
  - 動詞の使用ルール（REST APIでは避ける）
- エラーレスポンスの標準化
  - 一貫したエラーフォーマット
  - エラーコードの体系化
  - 詳細なエラーメッセージ
  - ユーザーが対応可能な情報提供
- バージョニング戦略
  - APIバージョンの管理方法（URL、ヘッダー、クエリパラメータ）
  - 破壊的変更の扱い
  - 非推奨（Deprecated）の明示
- ドキュメントとの整合性
  - OpenAPI/Swagger仕様との一致
  - コメント・型定義の正確性
  - 例の適切性
- 後方互換性の考慮
  - 既存クライアントへの影響評価
  - 破壊的変更の回避
  - 移行パスの提供

---

## 適用基準

### 使用する場合

- ✅ REST API追加・変更
- ✅ GraphQL API追加・変更
- ✅ ライブラリのpublic API追加・変更
- ✅ Webhookエンドポイント追加
- ✅ gRPC/Protocol Buffers定義変更

### 使用しない場合

- ❌ 内部関数のみの変更
- ❌ プライベートAPI変更
- ❌ 実装詳細の変更
- ❌ ドキュメントのみの変更

---

## 具体例

### ❌ 悪い例: RESTful原則違反

```javascript
// HTTPメソッドの誤用
app.get('/api/users/delete/:id', (req, res) => {
  // DELETEメソッドを使うべき
  User.delete(req.params.id);
  res.json({ success: true });
});

app.post('/api/getUsers', (req, res) => {
  // GETメソッドを使うべき
  const users = User.findAll();
  res.json(users);
});

// 動詞を含むURL
app.post('/api/users/create', (req, res) => {
  // /api/users でPOSTすべき
  const user = User.create(req.body);
  res.json(user);
});

// 不適切なステータスコード
app.get('/api/users/:id', (req, res) => {
  const user = User.find(req.params.id);
  if (!user) {
    // 404 Not Foundを使うべき
    res.status(200).json({ error: 'User not found' });
  }
  res.json(user);
});
```

**問題点**: HTTPメソッドの誤用、動詞を含むURL、不適切なステータスコードが使用されています。

### ✅ 良い例: RESTful設計

```javascript
// 適切なHTTPメソッドとリソース指向URL
app.get('/api/users', (req, res) => {
  const users = User.findAll();
  res.json(users);
});

app.get('/api/users/:id', (req, res) => {
  const user = User.find(req.params.id);
  if (!user) {
    return res.status(404).json({
      error: {
        code: 'USER_NOT_FOUND',
        message: 'User not found',
        details: { userId: req.params.id }
      }
    });
  }
  res.json(user);
});

app.post('/api/users', (req, res) => {
  const user = User.create(req.body);
  res.status(201).json(user);
});

app.put('/api/users/:id', (req, res) => {
  const user = User.update(req.params.id, req.body);
  res.json(user);
});

app.delete('/api/users/:id', (req, res) => {
  User.delete(req.params.id);
  res.status(204).send();
});
```

**理由**: 適切なHTTPメソッド、リソース指向のURL、適切なステータスコードを使用しています。

---

### ❌ 悪い例: エラーレスポンスの不統一

```python
# エンドポイント1
@app.route('/api/users/<id>')
def get_user(id):
    user = User.find(id)
    if not user:
        return {'error': 'not found'}, 404

# エンドポイント2
@app.route('/api/orders/<id>')
def get_order(id):
    order = Order.find(id)
    if not order:
        return {'message': 'Order does not exist'}, 404

# エンドポイント3
@app.route('/api/products/<id>')
def get_product(id):
    product = Product.find(id)
    if not product:
        return {'err_msg': 'Product not found', 'code': 404}, 404
```

**問題点**: エラーレスポンスの形式がエンドポイントごとに異なり、クライアント側での処理が困難です。

### ✅ 良い例: 標準化されたエラーレスポンス

```python
from flask import jsonify

class APIError(Exception):
    def __init__(self, code, message, status_code=400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'error': {
            'code': error.code,
            'message': error.message,
            'details': error.details
        }
    }
    return jsonify(response), error.status_code

@app.route('/api/users/<id>')
def get_user(id):
    user = User.find(id)
    if not user:
        raise APIError(
            code='USER_NOT_FOUND',
            message='User not found',
            status_code=404,
            details={'user_id': id}
        )
    return jsonify(user)

@app.route('/api/orders/<id>')
def get_order(id):
    order = Order.find(id)
    if not order:
        raise APIError(
            code='ORDER_NOT_FOUND',
            message='Order not found',
            status_code=404,
            details={'order_id': id}
        )
    return jsonify(order)
```

**理由**: すべてのエンドポイントで一貫したエラーフォーマットを使用し、クライアント側の処理を簡素化しています。

---

### ❌ 悪い例: バージョニングの欠如

```typescript
// v1の既存API
interface User {
  id: string;
  name: string;
}

app.get('/api/users/:id', (req, res) => {
  const user: User = getUserById(req.params.id);
  res.json(user);
});

// 破壊的変更（既存クライアントが壊れる）
interface User {
  id: string;
  firstName: string;  // nameから変更
  lastName: string;   // 新規追加
}

app.get('/api/users/:id', (req, res) => {
  const user: User = getUserById(req.params.id);
  res.json(user);
});
```

**問題点**: バージョニングなしで破壊的変更を行い、既存クライアントが壊れます。

### ✅ 良い例: 適切なバージョニング

```typescript
// v1 API（後方互換性維持）
interface UserV1 {
  id: string;
  name: string;
}

app.get('/api/v1/users/:id', (req, res) => {
  const user: UserV2 = getUserById(req.params.id);
  // v1形式に変換
  const userV1: UserV1 = {
    id: user.id,
    name: `${user.firstName} ${user.lastName}`
  };
  res.json(userV1);
});

// v2 API（新形式）
interface UserV2 {
  id: string;
  firstName: string;
  lastName: string;
}

app.get('/api/v2/users/:id', (req, res) => {
  const user: UserV2 = getUserById(req.params.id);
  res.json(user);
});
```

**理由**: バージョニングにより、既存クライアントの動作を保証しつつ新形式を提供しています。

---

### ❌ 悪い例: ライブラリAPIの不適切な設計

```python
# 設定オプションが分散
client = APIClient()
client.api_key = "xxx"
client.timeout = 30
client.retry_count = 3
client.set_base_url("https://api.example.com")

# メソッド名が一貫していない
client.getUser(123)      # get_user が適切
client.create_order({})  # createOrder と統一すべき
client.DeleteProduct(456) # 大文字小文字が不統一
```

**問題点**: 設定方法の不統一、命名規則の不統一が見られます。

### ✅ 良い例: 一貫したライブラリAPI設計

```python
# 設定をコンストラクタで一元化
client = APIClient(
    api_key="xxx",
    base_url="https://api.example.com",
    timeout=30,
    max_retries=3
)

# 一貫した命名規則（snake_case）
user = client.get_user(123)
order = client.create_order({})
client.delete_product(456)

# Fluent Interface（チェーン可能）
result = client \
    .with_timeout(60) \
    .with_retries(5) \
    .get_user(123)
```

**理由**: 設定の一元化、命名規則の統一、直感的なAPIにより使いやすさが向上しています。

---

## 2026年トレンド

API設計において以下のトレンドが見られます。

- GraphQLの普及（柔軟なデータ取得）
- OpenAPI/Swagger仕様の標準化
- gRPC/Protocol Buffersの高速通信
- Webhookのセキュリティ強化（署名検証）
- APIゲートウェイの活用（レート制限、認証、監視）

AI生成コードは、個別のエンドポイントは生成できても、API全体の一貫性や後方互換性を考慮しない傾向があります。

---

## 関連観点

- [D02] アーキテクチャパターン準拠
- [DOC02] ドキュメント整合性
- [C02] 機能要件の適合性
- [S01] セキュリティ脆弱性

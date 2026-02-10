# YAGNIチェック（拡張版）

**ID**: Q05
**カテゴリ**: 品質と保守性
**優先度**: Tier 2（推奨）⭐⭐⭐⭐
**信頼度基準**: 80-100点

---

## 参照元

- [obra/superpowers](https://github.com/obra/superpowers)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

YAGNI（You Aren't Gonna Need It）は、実際に必要になるまで機能を実装しないという原則です。本観点では、YAGNIチェックに加えて、DRY（Don't Repeat Yourself）、KISS（Keep It Simple, Stupid）原則を統合的に評価し、不要な複雑性、未使用コード、過剰な拡張性を検出します。特にAI生成コードは「将来の拡張性」を過剰に考慮する傾向があるため、実際の使用箇所を`grep`で確認することが重要です。

---

## チェック内容

- YAGNI違反の検出
  - 未使用のクラス、メソッド、関数
  - 実際に呼び出されていない拡張ポイント
  - 将来の要件に備えた過剰な抽象化
  - 使われていない設定オプション
- ハードコード値の検出
  - マジックナンバー
  - 設定ファイル化すべき値
  - 環境依存のハードコード
- DRY原則（重複コード）
  - 類似した処理の重複
  - コピー＆ペーストコード
  - 共通化可能なロジック
- KISS原則（過剰な複雑性）
  - 不必要に複雑な実装
  - シンプルな代替案が存在する場合
  - オーバーエンジニアリング

---

## 適用基準

### 使用する場合

- ✅ 新規機能追加
- ✅ 拡張性実装（インターフェース、抽象クラス等）
- ✅ 設定オプションの追加
- ✅ ユーティリティ関数の追加

### 使用しない場合

- ❌ 明確な要件に基づく実装
- ❌ 既存機能のリファクタリング
- ❌ バグ修正
- ❌ テストコード

---

## 具体例

### ❌ 悪い例: YAGNI違反（未使用の拡張性）

```python
class UserService:
    def __init__(self):
        self.strategies = {}  # 将来の拡張に備えた戦略パターン

    def register_strategy(self, name, strategy):
        # 実際には使われていない
        self.strategies[name] = strategy

    def get_strategy(self, name):
        # 実際には呼び出されていない
        return self.strategies.get(name)

    def create_user(self, data):
        # 実際の実装は単純
        return User(**data)
```

**問題点**: 戦略パターンの実装が追加されているが、実際には使われていません。`grep -r "register_strategy\|get_strategy"`で確認すると呼び出し箇所がゼロです。

### ✅ 良い例: シンプルな実装

```python
class UserService:
    def create_user(self, data):
        return User(**data)
```

**理由**: 実際に必要な機能のみを実装し、拡張性は実際に必要になった時点で追加します。

---

### ❌ 悪い例: ハードコード値

```javascript
function calculateDiscount(price, userType) {
  if (userType === 'premium') {
    return price * 0.8; // 20% off
  } else if (userType === 'standard') {
    return price * 0.9; // 10% off
  }
  return price;
}

function checkInventory(quantity) {
  if (quantity < 10) { // 閾値がハードコード
    return 'low';
  }
  return 'ok';
}
```

**問題点**: 割引率や在庫閾値がハードコードされており、変更時にコード修正が必要です。

### ✅ 良い例: 設定ファイル化

```javascript
// config.js
const DISCOUNT_RATES = {
  premium: 0.2,
  standard: 0.1,
};

const INVENTORY_THRESHOLD = 10;

// service.js
function calculateDiscount(price, userType) {
  const discountRate = DISCOUNT_RATES[userType] || 0;
  return price * (1 - discountRate);
}

function checkInventory(quantity) {
  if (quantity < INVENTORY_THRESHOLD) {
    return 'low';
  }
  return 'ok';
}
```

**理由**: 設定値を定数化することで、変更が容易になり、保守性が向上します。

---

### ❌ 悪い例: DRY違反（重複コード）

```python
def create_user_from_api(api_data):
    user = User()
    user.name = api_data.get('name', '')
    user.email = api_data.get('email', '')
    user.age = api_data.get('age', 0)
    user.created_at = datetime.now()
    return user

def create_user_from_form(form_data):
    user = User()
    user.name = form_data.get('name', '')
    user.email = form_data.get('email', '')
    user.age = form_data.get('age', 0)
    user.created_at = datetime.now()
    return user
```

**問題点**: ユーザー作成ロジックが重複しています。

### ✅ 良い例: 共通化

```python
def create_user(data):
    user = User()
    user.name = data.get('name', '')
    user.email = data.get('email', '')
    user.age = data.get('age', 0)
    user.created_at = datetime.now()
    return user

def create_user_from_api(api_data):
    return create_user(api_data)

def create_user_from_form(form_data):
    return create_user(form_data)
```

**理由**: 共通ロジックを抽出し、重複を排除しています。

---

### ❌ 悪い例: KISS違反（過剰な複雑性）

```typescript
interface DataTransformer<T, U> {
  transform(input: T): U;
}

class UserDataTransformerFactory {
  private transformers: Map<string, DataTransformer<any, any>> = new Map();

  register<T, U>(key: string, transformer: DataTransformer<T, U>) {
    this.transformers.set(key, transformer);
  }

  getTransformer<T, U>(key: string): DataTransformer<T, U> {
    return this.transformers.get(key) as DataTransformer<T, U>;
  }
}

// 実際の使用箇所
const factory = new UserDataTransformerFactory();
factory.register('user', {
  transform: (data) => ({ name: data.name, email: data.email })
});
const transformer = factory.getTransformer('user');
const result = transformer.transform(userData);
```

**問題点**: 単純なデータ変換に対して、ファクトリーパターンとジェネリクスを使用した過剰な抽象化が行われています。

### ✅ 良い例: シンプルな実装

```typescript
function transformUserData(data: any) {
  return { name: data.name, email: data.email };
}

const result = transformUserData(userData);
```

**理由**: 実際の要件に対してシンプルな関数で十分です。

---

## 2026年トレンド

AI生成コードは、以下の理由でYAGNI違反を引き起こしやすい傾向があります。

- 「良いコード」の例として学習した拡張性の高いパターンを過剰に適用
- 実際の使用箇所を確認せずに「将来使うかもしれない」機能を実装
- デザインパターンの教科書的な実装をそのまま適用

レビュー時には必ず以下を確認してください。

- `grep -r "メソッド名\|クラス名"`で実際の使用箇所を確認
- 本当に今必要な機能か問う
- シンプルな代替案が存在しないか検討

---

## 関連観点

- [Q04] アンチパターン
- [Q02] 複雑性
- [Q01] 読みやすさ
- [D02] アーキテクチャパターン準拠

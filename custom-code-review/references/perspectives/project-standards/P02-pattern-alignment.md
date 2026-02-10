# 既存パターンとの整合性

**ID**: P02
**カテゴリ**: プロジェクト標準
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)

---

## 概要

この観点は、新規実装が既存コードベースのアーキテクチャパターン、実装パターン、設計パターンと整合しているかを確認します。類似機能の実装方法を参照し、プロジェクト全体の設計思想と一貫性を保つことを目的とします。

新機能やアーキテクチャ変更の際に適用し、プロジェクトの「慣習」や「流儀」を維持することで、長期的な保守性を向上させます。

---

## チェック内容

- 類似機能の実装方法との一致
  - 既存の類似エンドポイント、コンポーネント、サービスの実装パターン
  - データフェッチング、状態管理、バリデーションの手法
- ディレクトリ構造の慣習遵守
  - 同種のファイルの配置場所
  - モジュール分割の粒度
- 依存関係管理パターンの統一
  - 依存性注入の方法
  - サービスロケーターパターンの使用
- 状態管理パターンの統一
  - Redux、Zustand、Context APIなどの使い分け
  - グローバル状態vsローカル状態の判断基準
- API設計パターンの統一
  - RESTful設計規約
  - レスポンス形式の統一
  - エラーハンドリングパターン
- データベースアクセスパターンの統一
  - ORM使用パターン
  - トランザクション管理
  - クエリビルダーの使い方
- テストパターンの統一
  - モックの作成方法
  - テストファイルの配置
  - テストユーティリティの使用

---

## 適用基準

### 使用する場合

- ✅ 新機能追加
- ✅ アーキテクチャ変更
- ✅ 新規コンポーネント追加
- ✅ 新規APIエンドポイント追加

### 使用しない場合

- ❌ 単純なバグ修正（既存パターンの変更なし）
- ❌ ドキュメント変更のみ
- ❌ テストコードのみの変更

---

## 具体例

### ❌ 悪い例

```typescript
// 既存のユーザーサービスは依存性注入を使用
class UserService {
  constructor(private db: Database, private cache: Cache) {}

  async getUser(id: string) {
    return this.cache.get(id) ?? await this.db.findUser(id);
  }
}

// 新規実装: 違反 - グローバル変数を直接参照
import { globalDb, globalCache } from './globals';

class ProductService {
  async getProduct(id: string) {
    return globalCache.get(id) ?? await globalDb.findProduct(id);
  }
}
```

**問題点**: 既存のUserServiceは依存性注入パターンを採用しているのに、新しいProductServiceはグローバル変数を直接参照しており、パターンの一貫性が失われています。

### ✅ 良い例

```typescript
// 既存パターンに従った実装
class ProductService {
  constructor(private db: Database, private cache: Cache) {}

  async getProduct(id: string) {
    return this.cache.get(id) ?? await this.db.findProduct(id);
  }
}
```

**理由**: 既存のUserServiceと同じ依存性注入パターンを採用しており、プロジェクト全体の設計思想と一貫性が保たれています。

---

### ❌ 悪い例

```python
# 既存のAPIエンドポイントは標準化されたレスポンス形式を使用
@app.route('/api/users/<id>')
def get_user(id):
    user = User.query.get(id)
    return jsonify({
        'success': True,
        'data': user.to_dict(),
        'timestamp': datetime.utcnow().isoformat()
    })

# 新規実装: 違反 - 異なるレスポンス形式
@app.route('/api/products/<id>')
def get_product(id):
    product = Product.query.get(id)
    return jsonify(product.to_dict())  # 標準形式と異なる
```

**問題点**: 既存のエンドポイントは`success`、`data`、`timestamp`を含む標準形式を使用しているのに、新しいエンドポイントは生のデータを返しています。

### ✅ 良い例

```python
@app.route('/api/products/<id>')
def get_product(id):
    product = Product.query.get(id)
    return jsonify({
        'success': True,
        'data': product.to_dict(),
        'timestamp': datetime.utcnow().isoformat()
    })
```

**理由**: 既存のレスポンス形式に従っており、フロントエンドのクライアントコードが統一的にレスポンスを処理できます。

---

## 関連観点

- [P01] AIエージェント向け指示の遵守
- [D02] アーキテクチャパターン準拠
- [D03] API設計

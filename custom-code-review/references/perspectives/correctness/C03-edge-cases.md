# エッジケースとバウンダリー条件

**ID**: C03
**カテゴリ**: 正確性（基本）
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Edge Cases and Error Handling: Where AI Code Falls Short](https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/)

---

## 概要

この観点は、極端な入力や境界条件での正しい動作を確認します。通常のハッピーパス以外のシナリオで、コードが期待通りに動作するか、適切にエラーハンドリングされているかをチェックします。

ユーザー入力処理、データ変換、境界値処理を含むコードで適用し、予期しない入力によるバグやクラッシュを防ぎます。

---

## チェック内容

- Null/undefined/空文字列の処理
  - Nullチェックの有無
  - 空文字列の扱い
  - Undefinedの処理
- 空配列/空オブジェクトの処理
  - 空配列への操作
  - 空オブジェクトのプロパティアクセス
  - イテレーション時の挙動
- 数値の境界値
  - ゼロの処理
  - 負数の処理
  - 最大値・最小値
  - NaN、Infinity の処理
- 文字列の境界値
  - 空文字列
  - 1文字の文字列
  - 最大長の文字列
  - 特殊文字を含む文字列
- 日時の境界値
  - タイムゾーンの考慮
  - うるう年・うるう秒
  - 夏時間の切り替え
  - Unix エポック境界
- ファイルサイズの制限
  - 空ファイル
  - 最大ファイルサイズ
  - 巨大ファイルの処理
- 同時実行の制限
  - 同時接続数の上限
  - レート制限
  - リソース枯渇
- ネットワークタイムアウト
  - 接続タイムアウト
  - 読み取りタイムアウト
  - リトライ処理

---

## 適用基準

### 使用する場合

- ✅ ユーザー入力処理
- ✅ データ変換処理
- ✅ 境界値処理
- ✅ 外部APIの呼び出し
- ✅ ファイル操作
- ✅ 数値計算

### 使用しない場合

- ❌ 内部のプライベート関数（引数が保証されている）
- ❌ 型安全言語で型による保証がある場合

---

## 具体例

### ❌ 悪い例：空配列の未処理

```javascript
function getAveragePrice(products) {
  const total = products.reduce((sum, p) => sum + p.price, 0);
  // 問題: products が空配列の場合、ゼロ除算
  return total / products.length;
}
```

**問題点**: 空配列が渡された場合、`0 / 0`となり`NaN`が返されます。

### ✅ 良い例

```javascript
function getAveragePrice(products) {
  if (products.length === 0) {
    return 0;  // または null、デフォルト値など
  }

  const total = products.reduce((sum, p) => sum + p.price, 0);
  return total / products.length;
}
```

**理由**: 空配列のケースを明示的に処理しています。

---

### ❌ 悪い例：負数の未考慮

```python
def calculate_discount_percentage(original_price, discounted_price):
    # 問題: 負数や0の場合を考慮していない
    return (original_price - discounted_price) / original_price * 100
```

**問題点**: `original_price`が0の場合はゼロ除算、負数の場合は不正な計算結果になります。

### ✅ 良い例

```python
def calculate_discount_percentage(original_price, discounted_price):
    if original_price <= 0:
        raise ValueError("Original price must be positive")

    if discounted_price < 0:
        raise ValueError("Discounted price cannot be negative")

    if discounted_price > original_price:
        raise ValueError("Discounted price cannot exceed original price")

    return (original_price - discounted_price) / original_price * 100
```

**理由**: すべての境界値とエッジケースをバリデーションで検証しています。

---

### ❌ 悪い例：特殊文字の未処理

```typescript
function createSlug(title: string): string {
  // 問題: 空文字列、特殊文字、複数スペースを考慮していない
  return title.toLowerCase().replace(/ /g, '-');
}

// "  Hello   World!!  " → "--hello---world!!--"
```

**問題点**: 連続スペース、前後の空白、特殊文字が適切に処理されません。

### ✅ 良い例

```typescript
function createSlug(title: string): string {
  if (!title || title.trim().length === 0) {
    throw new Error("Title cannot be empty");
  }

  return title
    .trim()
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')  // 特殊文字を削除
    .replace(/\s+/g, '-')       // 連続スペースを1つのハイフンに
    .replace(/-+/g, '-')        // 連続ハイフンを1つに
    .replace(/^-+|-+$/g, '');   // 前後のハイフンを削除
}

// "  Hello   World!!  " → "hello-world"
```

**理由**: すべてのエッジケースを考慮した堅牢な実装です。

---

### ❌ 悪い例：タイムアウトの未設定

```python
import requests

def fetch_user_data(user_id):
    # 問題: タイムアウトが設定されていない
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

**問題点**: サーバーが応答しない場合、プログラムが無期限に待機します。

### ✅ 良い例

```python
import requests
from requests.exceptions import Timeout, RequestException

def fetch_user_data(user_id, timeout=5):
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Timeout:
        raise Exception(f"Request timed out after {timeout} seconds")
    except RequestException as e:
        raise Exception(f"Failed to fetch user data: {str(e)}")
```

**理由**: タイムアウトを設定し、エラーハンドリングも適切に行っています。

---

### ❌ 悪い例：Null/undefined の未チェック

```typescript
function getUserDisplayName(user) {
  // 問題: user や user.profile が null/undefined の可能性
  return user.profile.firstName + ' ' + user.profile.lastName;
}
```

**問題点**: `user`または`user.profile`がnullの場合、実行時エラーになります。

### ✅ 良い例

```typescript
function getUserDisplayName(user): string {
  if (!user) {
    return 'Anonymous';
  }

  if (!user.profile) {
    return user.email ?? 'Unknown User';
  }

  const firstName = user.profile.firstName ?? '';
  const lastName = user.profile.lastName ?? '';

  return `${firstName} ${lastName}`.trim() || user.email || 'Unknown User';
}
```

**理由**: すべてのNull/undefinedケースを考慮し、適切なフォールバック値を提供しています。

---

## 2026年トレンド

AI生成コードは「ハッピーパス」の実装に強いですが、エッジケースやエラー処理の実装が不十分な傾向があります。特にNull処理、空配列、境界値のバリデーションに注意が必要です。

---

## 関連観点

- [C01] バグ検出
- [C04] サイレントフェイラー
- [T03] エラーハンドリング品質

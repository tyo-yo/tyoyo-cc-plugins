# バグ検出

**ID**: C01
**カテゴリ**: 正確性（基本）
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点（必ず発生）、80-90点（高確率）

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Code Review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)
- すべての公式プラグイン

---

## 概要

この観点は、コード内のロジックエラー、実行時エラー、機能不全を特定します。コードレビューの最も基本的かつ重要な観点であり、実際のバグが本番環境に到達することを防ぎます。

すべてのコード変更で適用され、実行時に確実に発生するエラーや高確率で発生するバグを検出することに焦点を当てます。

---

## チェック内容

- ロジックエラー
  - 条件式の誤り（`&&` vs `||`、`==` vs `===`）
  - 演算子の誤用（`+` vs `-`、`*` vs `/`）
  - 分岐条件の抜け漏れ
- Null/undefined参照
  - オプショナルチェーンの欠如
  - Null安全性の欠如
  - デフォルト値の未設定
- 配列境界エラー
  - インデックスアウトオブバウンズ
  - 空配列への操作
  - 負のインデックス
- 型エラー
  - 型キャストの誤り
  - 型安全性の欠如
  - 期待される型と実際の型の不一致
- メモリリーク
  - クリーンアップされないリソース
  - イベントリスナーの解除漏れ
  - タイマーのクリア漏れ
- 競合状態
  - 非同期処理の順序依存
  - 共有状態への競合アクセス
- 無限ループ
  - 終了条件の欠如
  - 無限再帰
- Off-by-one エラー
  - ループの境界条件の誤り
  - 配列スライスの範囲誤り
- 初期化エラー
  - 未初期化変数の使用
  - 初期化順序の誤り

---

## 適用基準

### 使用する場合

- ✅ 常に適用（すべてのコード変更）

### 使用しない場合

- ❌ 該当なし（必須観点）

---

## 具体例

### ❌ 悪い例：Null参照エラー

```typescript
function getUserEmail(user: User): string {
  // user.profile が null/undefined の場合クラッシュ
  return user.profile.email;
}
```

**問題点**: `user.profile`がnullまたはundefinedの場合、実行時エラーが発生します。

### ✅ 良い例

```typescript
function getUserEmail(user: User): string | null {
  return user.profile?.email ?? null;
}
```

**理由**: オプショナルチェーンとNull合体演算子を使用して安全にアクセスしています。

---

### ❌ 悪い例：Off-by-one エラー

```python
def get_last_n_items(items, n):
    # n=3 の場合、実際には4つの要素を取得してしまう
    return items[len(items) - n:]
```

**問題点**: スライスの開始位置が誤っており、期待より1つ多い要素を取得します。

### ✅ 良い例

```python
def get_last_n_items(items, n):
    return items[-n:] if n > 0 else []
```

**理由**: Pythonの負のインデックスを正しく使用し、エッジケースも考慮しています。

---

### ❌ 悪い例：ロジックエラー

```javascript
function canAccessResource(user, resource) {
  // 意図: 管理者 OR リソースのオーナー
  // 実装: 管理者 AND リソースのオーナー（誤り）
  if (user.isAdmin && resource.ownerId === user.id) {
    return true;
  }
  return false;
}
```

**問題点**: `&&`を使用しているため、管理者かつオーナーの場合のみtrueになり、本来の意図と異なります。

### ✅ 良い例

```javascript
function canAccessResource(user, resource) {
  return user.isAdmin || resource.ownerId === user.id;
}
```

**理由**: `||`を使用して正しいOR条件を実装しています。

---

### ❌ 悪い例：競合状態

```typescript
let counter = 0;

async function incrementCounter() {
  const current = counter;
  await someAsyncOperation();
  counter = current + 1;  // 競合状態
}
```

**問題点**: 複数の非同期呼び出しが同時に実行されると、counterの値が正しくインクリメントされない可能性があります。

### ✅ 良い例

```typescript
let counter = 0;

async function incrementCounter() {
  await someAsyncOperation();
  counter++;  // アトミックな操作
}
```

**理由**: インクリメント操作をアトミックに実行し、競合状態を回避しています。

---

## 2026年トレンド

AIコード生成ツールはハッピーパスの実装に強いですが、エッジケースやエラー処理でバグを生む傾向があります。特にNull参照、配列境界、競合状態に注意が必要です。

---

## 関連観点

- [C03] エッジケースとバウンダリー条件
- [C04] サイレントフェイラー
- [C05] 例外安全性
- [T01] テストカバレッジ

# パフォーマンス

**ID**: PERF01
**カテゴリ**: パフォーマンス
**優先度**: Tier 3（オプション）
**信頼度基準**: 85-100点（明らか）、70-84点（潜在的）

---

## 参照元

- [8 Best AI Code Review Tools That Catch Real Bugs in 2026](https://www.qodo.ai/blog/best-ai-code-review-tools-2026/)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

明らかなパフォーマンスボトルネックや非効率性を検出する観点。**重要**: この観点はパフォーマンスクリティカルなコードパスのみを対象とする。理論的な速度改善や微細な最適化は避け、実際のユーザー体験に影響を与える問題に焦点を当てる。

2026年のトレンドとして、AIツールは「動作するコード」を素早く生成できるが、パフォーマンス最適化までは考慮されないことが多い。この観点では、実際のボトルネックとなり得る問題を特定する。

---

## チェック内容

- **無限ループや終了しないループ**: ユーザー入力次第で無限ループになるケース
- **N+1クエリ問題**: データベースアクセスの非効率性
- **過剰なメモリ割り当て**: 不要な大量オブジェクト生成
- **不要なネットワークリクエスト**: 複数回の冗長なAPI呼び出し
- **高コストな操作の繰り返し**: ループ内での不必要な再計算
- **キャッシング機会の欠如**: 同じ計算を繰り返す
- **データベースインデックスの欠如**: フルテーブルスキャンが発生するクエリ
- **大量データの非効率な処理**: ページネーションやストリーミング処理の欠如

---

## 適用基準

### 使用する場合

- ✅ パフォーマンスクリティカルなパス（ホットパス）
- ✅ データベースクエリの変更
- ✅ ループ処理の追加・変更
- ✅ 外部API呼び出し
- ✅ ファイル処理、データ変換
- ✅ ユーザーのインタラクティブな操作に影響する箇所

### 使用しない場合

- ❌ 初期化コード（起動時に1回のみ実行）
- ❌ バッチ処理（非同期処理で許容範囲）
- ❌ 理論的な最適化（実測なし）
- ❌ マイクロ最適化（可読性を犠牲にする）

---

## 具体例

### ❌ 悪い例1: N+1クエリ問題

```typescript
// ユーザーごとに投稿を取得（N+1問題）
async function getUsersWithPosts() {
  const users = await db.users.findAll();

  for (const user of users) {
    // 各ユーザーごとにクエリを発行（非効率）
    user.posts = await db.posts.findAll({ userId: user.id });
  }

  return users;
}
```

**問題点**: 100人のユーザーがいる場合、101回のクエリが発行される（1回 + 100回）。

### ❌ 悪い例2: ループ内での不要な再計算

```typescript
function calculateTotals(items: Item[]) {
  const results = [];

  for (const item of items) {
    // ループの度に同じ税率計算を実行（無駄）
    const taxRate = getTaxRateFromDatabase(item.category);
    results.push(item.price * (1 + taxRate));
  }

  return results;
}
```

**問題点**: カテゴリごとの税率は固定なのに、ループの度にデータベース問い合わせを実行。

### ❌ 悪い例3: 大量データの一括ロード

```typescript
// 全ユーザーを一度にメモリにロード（メモリ不足のリスク）
async function exportAllUsers() {
  const users = await db.users.findAll(); // 100万件

  return users.map(user => formatUser(user));
}
```

**問題点**: 大量データを一度にロードするとメモリ不足やタイムアウトが発生する。

### ✅ 良い例1: JOIN句で一括取得（N+1問題の解決）

```typescript
// JOINで一括取得（効率的）
async function getUsersWithPosts() {
  const users = await db.users.findAll({
    include: [{ model: db.posts }]
  });

  return users; // 1回のクエリで完了
}
```

**理由**: JOINを使うことで、データベースへのクエリが1回で済む。

### ✅ 良い例2: ループ外で計算（キャッシング）

```typescript
function calculateTotals(items: Item[]) {
  // カテゴリごとの税率を事前に取得
  const taxRates = new Map<string, number>();

  for (const item of items) {
    if (!taxRates.has(item.category)) {
      taxRates.set(item.category, getTaxRateFromDatabase(item.category));
    }
  }

  // 計算時はMapから取得（高速）
  return items.map(item => {
    const taxRate = taxRates.get(item.category)!;
    return item.price * (1 + taxRate);
  });
}
```

**理由**: 同じカテゴリの税率を再計算せず、Mapにキャッシュして再利用。

### ✅ 良い例3: ストリーミング処理（メモリ効率）

```typescript
// ページネーションで分割処理（メモリ効率的）
async function* exportAllUsers() {
  const PAGE_SIZE = 1000;
  let offset = 0;

  while (true) {
    const users = await db.users.findAll({
      limit: PAGE_SIZE,
      offset
    });

    if (users.length === 0) break;

    yield users.map(user => formatUser(user));
    offset += PAGE_SIZE;
  }
}
```

**理由**: ジェネレータとページネーションでメモリ使用量を抑え、大量データを安全に処理。

---

## 2026年トレンド

AI生成コードは「動作する」ことを優先し、パフォーマンスは二の次になりがち。特にN+1クエリやループ内での不要な計算は頻出パターン。

この観点では、理論的な最適化（例: `for`ループを`forEach`に変える）ではなく、実際のボトルネックとなる問題（データベースアクセス、API呼び出し、メモリ使用量）に焦点を当てる。

---

## 関連観点

- [PERF03] リソース管理
- [C01] バグ検出
- [Q02] 複雑性

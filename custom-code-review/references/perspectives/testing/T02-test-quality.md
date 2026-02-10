# テストの質

**ID**: T02
**カテゴリ**: テストとエラー処理
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)

---

## 概要

テストの質は、テストコード自体の設計品質を評価します。良いテストは、実装の詳細ではなく振る舞いに焦点を当て、リファクタリング後も有効に機能し続けます。

テストが独立性、決定性（非決定的テストの排除）、明確性（AAA: Arrange-Act-Assert）、適切なアサーション、保守性を持つかを確認します。

---

## チェック内容

- リファクタリング後も有効か（実装詳細に依存していないか）
  - 公開インターフェースのみをテスト
  - 内部実装の変更に影響されない
  - プライベートメソッドへの直接依存回避
- テストの独立性
  - 他のテストに依存しない
  - 実行順序に依存しない
  - グローバル状態を共有しない
- テストの決定性（非決定的テストの排除）
  - 時刻に依存しない（モック使用）
  - ランダム値に依存しない（固定値使用）
  - 外部サービスに依存しない（スタブ使用）
- テストの明確性（AAA: Arrange-Act-Assert）
  - Arrange（準備）: テスト対象の初期化
  - Act（実行）: テスト対象の操作
  - Assert（検証）: 結果の確認
- 適切なアサーション
  - 具体的なアサーション（例: `toBe(5)` vs `toBeDefined()`）
  - エラーメッセージの検証
  - 複数の関連する検証
- テストの保守性
  - テストヘルパーの適切な使用
  - 重複の排除
  - 明確なテスト名

---

## 適用基準

### 使用する場合

- ✅ テストコード変更
- ✅ テスト追加
- ✅ テストリファクタリング

### 使用しない場合

- ❌ 本番コードのみの変更（テストコード変更なし）

---

## 具体例

### ❌ 悪い例

```typescript
// 実装詳細に依存した脆弱なテスト
test('user service', () => {
  const service = new UserService();
  // プライベートメソッドを直接テスト
  expect(service['_validateEmail']('test@example.com')).toBe(true);
  // 内部状態に依存
  expect(service['_cache'].size).toBe(0);
});

// 非決定的テスト
test('generates timestamp', () => {
  const result = generateReport();
  expect(result.timestamp).toBe(Date.now()); // 失敗する可能性あり
});

// 不明確なテスト
test('test1', () => {
  const x = new Thing();
  x.doStuff();
  expect(x.value).toBe(10);
  x.doMoreStuff();
  expect(x.value).toBe(20);
});
```

**問題点**: 実装詳細への依存、非決定性、不明確な構造。

### ✅ 良い例

```typescript
// 公開インターフェースのみをテスト
test('creates valid user with email', () => {
  // Arrange
  const service = new UserService();
  const email = 'test@example.com';

  // Act
  const user = service.createUser({ email });

  // Assert
  expect(user.email).toBe(email);
  expect(user.isValid).toBe(true);
});

// 決定的テスト（時刻をモック）
test('generates report with fixed timestamp', () => {
  // Arrange
  const fixedDate = new Date('2026-01-01T00:00:00Z');
  jest.useFakeTimers();
  jest.setSystemTime(fixedDate);

  // Act
  const result = generateReport();

  // Assert
  expect(result.timestamp).toBe(fixedDate.getTime());

  // Cleanup
  jest.useRealTimers();
});

// 明確な構造（AAA）
describe('Counter', () => {
  test('increments value by one', () => {
    // Arrange
    const counter = new Counter(0);

    // Act
    counter.increment();

    // Assert
    expect(counter.value).toBe(1);
  });

  test('decrements value by one', () => {
    // Arrange
    const counter = new Counter(10);

    // Act
    counter.decrement();

    // Assert
    expect(counter.value).toBe(9);
  });
});
```

**理由**: 公開インターフェース、決定性、明確なAAA構造、独立性を満たしている。

---

## 関連観点

- [T01] テストカバレッジ
- [Q01] 読みやすさ
- [D01] 型設計とカプセル化

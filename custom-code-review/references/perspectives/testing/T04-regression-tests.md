# リグレッションテスト

**ID**: T04
**カテゴリ**: テストとエラー処理
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)

---

## 概要

リグレッションテストは、過去に発生したバグが再発しないことを確認するテストです。バグ修正PRでは、そのバグを再現し、修正後に失敗しないテストケースを追加することが重要です。

特に、過去にバグが多かった箇所や、変更頻度の高いファイル（ホットスポット）では、リグレッションテストの有無を確認します。

---

## チェック内容

- バグ修正PRでのテスト追加
  - バグを再現するテストケース
  - 修正後に成功するテスト
  - エッジケースのカバー
- 過去のバグ再発防止
  - 既知のバグパターンのテスト
  - 類似した条件でのテスト
- ホットスポット（変更頻度の高いファイル）のカバー
  - Git履歴から頻繁に修正される箇所を特定
  - その箇所のテストカバレッジ確認
- エッジケースの網羅
  - バグが発生した境界値
  - 特殊な入力パターン
- テストの明確な命名
  - バグのチケット番号を含む（例: `test_issue_1234_null_pointer_fix`）
  - 何をテストするかが明確

---

## 適用基準

### 使用する場合

- ✅ バグ修正PR
- ✅ 過去にバグがあった箇所の変更
- ✅ ホットスポット（変更頻度の高いファイル）の変更

### 使用しない場合

- ❌ 新規機能追加（バグ修正でない）
- ❌ リファクタリングのみ（動作変更なし）

---

## 具体例

### ❌ 悪い例

```typescript
// バグ修正: ユーザー名がnullの場合にクラッシュする問題
function displayUserName(user: User | null): string {
  // 修正: nullチェック追加
  if (!user) {
    return 'Guest';
  }
  return user.name;
}

// テストなし、または既存テストのみ
test('displays user name', () => {
  const user = { name: 'Alice' };
  expect(displayUserName(user)).toBe('Alice');
});
```

**問題点**: バグ修正に対応するリグレッションテストがない。nullケースのテストが欠如。

### ✅ 良い例

```typescript
// バグ修正: ユーザー名がnullの場合にクラッシュする問題（Issue #1234）
function displayUserName(user: User | null): string {
  // 修正: nullチェック追加
  if (!user) {
    return 'Guest';
  }
  return user.name;
}

// リグレッションテスト追加
describe('displayUserName', () => {
  test('displays user name for valid user', () => {
    const user = { name: 'Alice' };
    expect(displayUserName(user)).toBe('Alice');
  });

  // バグ再発防止テスト
  test('issue #1234: handles null user without crashing', () => {
    expect(displayUserName(null)).toBe('Guest');
  });

  test('issue #1234: handles undefined user without crashing', () => {
    expect(displayUserName(undefined as any)).toBe('Guest');
  });

  test('issue #1234: handles user with null name', () => {
    const user = { name: null as any };
    expect(displayUserName(user)).toBe(null);
  });
});
```

**理由**: バグを再現するテストケース（nullケース）を追加し、チケット番号を明記して再発防止。

---

## Git履歴からの問題パターン検出

リグレッションテストが特に重要な箇所は、Git履歴から特定できます。

```bash
# 変更頻度の高いファイル（ホットスポット）
git log --format=format: --name-only | \
  grep -v '^$' | sort | uniq -c | sort -rn | head -20

# 特定ファイルのバグ修正コミット
git log --grep="fix\|bug" --oneline -- path/to/file.ts
```

これらのファイルは、過去にバグが多かった可能性が高いため、リグレッションテストの追加が推奨されます。

---

## 関連観点

- [T01] テストカバレッジ
- [CTX01] Git履歴分析
- [C01] バグ検出

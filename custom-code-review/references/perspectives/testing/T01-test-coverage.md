# テストカバレッジ

**ID**: T01
**カテゴリ**: テストとエラー処理
**優先度**: Tier 1（必須）
**信頼度基準**: 80-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [matsengrp/plugins](https://github.com/matsengrp/plugins)

---

## 概要

テストカバレッジは、新規機能やロジック変更に対して、単なる行カバレッジではなく「振る舞いベース」の品質を評価します。重要なのは、エラーハンドリングパス、境界値、エッジケース、負のテストケース（失敗パス）が適切にカバーされているかです。

行カバレッジツールの数値だけでなく、ビジネスロジックの分岐や統合ポイントが実際にテストされているかを確認します。

---

## チェック内容

- エラーハンドリングパスのテスト
  - Try-catchブロックの失敗パス
  - エラーコールバックの動作確認
- 境界値とエッジケースのテスト
  - Null/undefined/空文字列
  - 数値の最大値/最小値/0
  - 空配列・空オブジェクト
- ビジネスロジック分岐のカバー
  - If文の両方のパス
  - Switch文のすべてのケース
  - 三項演算子の両方の結果
- 負のテストケース（失敗パス）
  - 不正な入力に対する拒否
  - 権限不足の場合の動作
- 統合テストの適切性
  - 外部サービスとの統合
  - データベース操作の確認
- テストの振る舞い焦点（実装詳細ではなく）
  - 公開インターフェースのテスト
  - 内部実装への依存回避

---

## 適用基準

### 使用する場合

- ✅ 新規機能追加
- ✅ ロジック変更
- ✅ エラーハンドリング追加

### 使用しない場合

- ❌ ドキュメント変更のみ
- ❌ コメント追加のみ
- ❌ フォーマット変更のみ

---

## 具体例

### ❌ 悪い例

```typescript
// テスト対象
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero');
  }
  return a / b;
}

// テスト: ハッピーパスのみ
test('divide two numbers', () => {
  expect(divide(10, 2)).toBe(5);
});
```

**問題点**: エラーハンドリングパス（ゼロ除算）がテストされていない。

### ✅ 良い例

```typescript
// テスト対象
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero');
  }
  return a / b;
}

// テスト: 正常系と異常系の両方
describe('divide', () => {
  test('divides two numbers correctly', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('throws error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  test('handles negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });
});
```

**理由**: 正常系、異常系（エラーパス）、境界値（負の数）をすべてカバーしている。

---

## 重大度評価

テスト不足の重大度は以下の基準で評価します。

- **9-10点**: データ喪失やセキュリティにつながる重大機能
- **5-8点**: ユーザー影響のある重要ロジック
- **1-4点**: 補完的カバレッジ

---

## 出力フォーマット

```markdown
**Test Gap**: [未カバー項目]
- **Severity**: [1-10]
- **Location**: [ファイルパス:行番号]
- **Risk**: [リスク説明]
- **Missing test**: [必要なテストケース]
- **Suggested test**: [テストコード例]
- **Confidence**: [スコア]
```

---

## 関連観点

- [T02] テストの質
- [T03] エラーハンドリング品質
- [C03] エッジケースとバウンダリー条件

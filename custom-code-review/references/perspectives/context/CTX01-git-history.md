# Git履歴分析

**ID**: CTX01
**カテゴリ**: コンテキスト分析
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [Code Review Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

Git履歴を分析し、過去の変更パターンから潜在的な問題を検出する観点。同じファイルや関数で繰り返されるバグ修正、リファクタリング後の不整合、過去に削除されたが復活した問題コード等を特定する。

この観点は、コード自体ではなく**変更の文脈**に焦点を当てる。過去の履歴から学ぶことで、将来のバグを予防できる。

---

## チェック内容

- **バグの温床検出**: 同じファイルで繰り返されるバグ修正
- **リファクタリング後の不整合**: 過去のリファクタリングで見逃された箇所
- **削除されたコードの復活**: 過去に問題があって削除されたコードが再導入されていないか
- **コミットメッセージとの整合性**: PR内容とコミットメッセージの一致
- **変更頻度の高いファイル**: ホットスポットの特定（変更が集中する箇所）
- **同じ作者の過去の問題**: 特定の開発者が繰り返す問題パターン
- **過去のセキュリティ修正の再発**: CVE修正箇所の再発防止

---

## 適用基準

### 使用する場合

- ✅ 変更頻度の高いファイル（月に5回以上変更）
- ✅ 過去にバグが多かった箇所
- ✅ 過去にセキュリティ修正があったファイル
- ✅ 大規模リファクタリング後の変更
- ✅ レガシーコードの修正

### 使用しない場合

- ❌ 新規ファイル作成（履歴がない）
- ❌ 初回コミット
- ❌ テストファイルのみの変更
- ❌ ドキュメント変更のみ

---

## 具体例

### ❌ 悪い例1: 繰り返されるバグ

**Git履歴**:
```
commit abc123: fix: null pointer in getUserProfile
commit def456: fix: handle undefined user in getUserProfile
commit ghi789: fix: add null check to getUserProfile
```

**現在の変更**:
```typescript
function getUserProfile(userId: string) {
  const user = database.findUser(userId);
  return user.profile; // また同じ箇所でnullチェックなし
}
```

**問題点**: 同じ関数で3回もバグ修正が繰り返されている。根本的な問題（型設計やエラーハンドリング）が解決されていない。

### ❌ 悪い例2: 削除されたコードの復活

**過去のコミット**:
```
commit xyz123: fix: remove insecure dynamic code execution
```

**現在の変更**:
```javascript
// 過去に削除された動的コード実行が復活
function executeUserScript(code) {
  return new Function(code)(); // セキュリティ問題が再発
}
```

**問題点**: 過去にセキュリティ理由で削除されたコードが再導入されている。

### ❌ 悪い例3: リファクタリング後の見逃し

**過去のコミット**:
```
commit aaa111: refactor: rename calculateTotal to computeSum
```

**現在の変更**:
```javascript
// 古い関数名を使用
const total = calculateTotal(items); // リファクタリング漏れ
```

**問題点**: リファクタリング時に一部のファイルが更新されず、古い関数名が残っている。

### ✅ 良い例1: 過去の問題から学ぶ

**Git履歴分析**:
```
commit abc123: fix: null pointer in getUserProfile
commit def456: fix: handle undefined user in getUserProfile
```

**推奨アクション**:
```typescript
// 型システムで根本的に解決
function getUserProfile(userId: string): UserProfile | null {
  const user = database.findUser(userId);

  if (!user) {
    return null; // 明示的にnullを返す
  }

  return user.profile;
}

// 呼び出し側で必ずnullチェック
const profile = getUserProfile(userId);
if (!profile) {
  throw new Error('User not found');
}
```

**理由**: 過去の繰り返されるバグから学び、型システムで根本的に解決。

### ✅ 良い例2: セキュリティ修正の履歴を確認

**過去のコミット**:
```
commit xyz123: fix: remove insecure code execution (CVE-2024-1234)
```

**レビュー時の確認**:
```markdown
**警告**: このファイルは過去にCVE-2024-1234で修正されています。
現在の変更がセキュリティリグレッションを引き起こさないか確認してください。

- 動的コード実行: ❌ 絶対に使用しない
- Function() の使用: ⚠️ 必要性を確認
- 動的評価: ⚠️ サンドボックス化を検討
```

**理由**: 過去のセキュリティ修正を踏まえ、同様の問題が再発しないよう警告。

### ✅ 良い例3: ホットスポットを特定

**Git履歴分析**:
```bash
$ git log --oneline --follow src/auth/login.ts | wc -l
42  # 過去6ヶ月で42回変更されている

$ git log --oneline --all --format='%aN' src/auth/login.ts | sort | uniq -c
  15 Alice
  12 Bob
   8 Charlie
   7 David
```

**レビュー時の推奨**:
```markdown
**ホットスポット検出**: `src/auth/login.ts`は変更頻度が非常に高い（42回/6ヶ月）

推奨アクション:
- リファクタリングを検討（単一責任の原則違反の可能性）
- テストカバレッジを強化
- 複数人が触る箇所なので、ドキュメント化を推奨
```

**理由**: 変更頻度の高いファイルは複雑性が高く、バグが混入しやすい。

### ✅ 良い例4: コミットメッセージとの整合性確認

**コミットメッセージ**:
```
fix: prevent SQL injection in user search
```

**変更内容**:
```typescript
// プリペアドステートメントを使用
const users = await db.query(
  'SELECT * FROM users WHERE name = ?',
  [searchQuery]
);
```

**レビュー確認**:
```markdown
✅ コミットメッセージと変更内容が一致
- 目的: SQLインジェクション防止
- 実装: プリペアドステートメント使用
- 結果: 期待通り
```

**理由**: コミットメッセージとコード変更が一致し、意図が明確。

---

## 関連観点

- [CTX02] コードベース理解
- [C01] バグ検出
- [S07] セキュリティリグレッション
- [T04] リグレッションテスト

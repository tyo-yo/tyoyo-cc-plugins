# コメント品質と精度

**ID**: DOC01
**カテゴリ**: ドキュメント
**優先度**: Tier 2（推奨）
**信頼度基準**: 91-100点（不正確）、80-90点（誤解招く）

---

## 参照元

- [PR Review Toolkit - comment-analyzer](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Claude Code Best Practices for Local Code Review](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)

---

## 概要

コード内のコメントの精度と有用性を評価する観点。AIが自動生成するコメントは「何をしているか」の自明な説明に偏りがちで、人間が本当に必要とする「なぜそうしているか」の説明が欠けることが多い。

この観点では、コメントが実装と矛盾していないか、誤解を招く表現がないか、そして長期的な価値があるかを評価する。自明なコメントや陳腐化したコメントは削除候補として特定する。

---

## チェック内容

- **事実検証**: 関数署名、戻り値、型参照が実装と一致しているか
- **完全性評価**: 前提条件、副作用、エラー処理について説明があるか
- **長期価値評価**: 「なぜ」の説明を重視、自明なコメントは削除対象
  - ❌ 悪い例: `// iをインクリメント` → コードを読めば分かる
  - ✅ 良い例: `// オフセットを調整してUTC時刻に変換` → 意図を説明
- **誤解要因の特定**: 曖昧性、古い参照、実装との矛盾
- **AIコメントの過剰性チェック**: 無駄な説明が多すぎないか
- **複雑なロジックのコメント不足**: 理解が困難な箇所に説明があるか

---

## 適用基準

### 使用する場合

- ✅ コメント追加・変更
- ✅ 複雑なロジックの実装
- ✅ 公開APIの変更
- ✅ AIが自動生成したコメントを含む

### 使用しない場合

- ❌ コメントがない単純なコード
- ❌ ドキュメント変更のみ（コード内コメント以外）
- ❌ テストコードのみの変更

---

## 具体例

### ❌ 悪い例1: 自明なコメント

```typescript
// ユーザーIDを取得
const userId = user.id;

// エラーをログに出力
console.error(error);

// 結果を返す
return result;
```

**問題点**: コードを読めば分かる内容を繰り返しているだけで、価値がない。

### ❌ 悪い例2: 実装と矛盾するコメント

```typescript
/**
 * ユーザーを作成する
 * @returns {Promise<User>} 作成されたユーザー
 */
async function createUser(data: UserInput): Promise<void> {
  // 実際は void を返すのでコメントが誤り
  await db.users.insert(data);
}
```

**問題点**: 戻り値の型がコメントと実装で一致していない。

### ❌ 悪い例3: 陳腐化したコメント

```typescript
// TODO: 後でバリデーションを追加
function processData(data: string) {
  // 実際には既にバリデーションが実装済み
  if (!data || data.length === 0) {
    throw new Error('Invalid data');
  }
  // ...
}
```

**問題点**: コメントが古く、実装の現状を反映していない。

### ✅ 良い例1: 意図を説明

```typescript
// タイムゾーンオフセットを考慮してUTC時刻に変換
// 注: サーバーとクライアントの時刻差を補正する必要がある
const utcTime = localTime + timezoneOffset;

// 再試行回数を3回に制限（API制限対策）
const MAX_RETRIES = 3;
```

**理由**: 「なぜ」その値や処理が必要かを説明している。

### ✅ 良い例2: 前提条件と副作用を明示

```typescript
/**
 * ユーザーセッションをクリーンアップする
 *
 * 前提条件: ユーザーが既にログアウト済みであること
 * 副作用: データベースのセッションレコードを物理削除
 * エラー: セッションが見つからない場合は何もしない（冪等性）
 */
async function cleanupSession(sessionId: string): Promise<void> {
  await db.sessions.delete({ id: sessionId });
}
```

**理由**: 関数の振る舞いを包括的に説明し、呼び出し側の理解を助ける。

### ✅ 良い例3: 複雑なロジックを補足

```typescript
// ソートアルゴリズム: Quick Select（平均O(n)）
// 理由: 全体ソート（O(n log n)）より高速で、中央値のみ必要なため
function findMedian(arr: number[]): number {
  const mid = Math.floor(arr.length / 2);
  return quickSelect(arr, mid);
}
```

**理由**: アルゴリズムの選択理由を明示し、将来の変更時の判断材料を提供。

---

## 2026年トレンド

AI生成コードは自明なコメントを大量生成する傾向がある。Claude Codeやその他のAIツールでコードを書く際、「何を」しているかは明白だが「なぜ」そうするかが不明なコメントが増加している。

この観点では、AIが追加した無駄なコメントを削除候補として指摘し、本当に価値のあるコメント（意図、前提条件、副作用、トレードオフ）を追加するよう推奨する。

---

## 関連観点

- [DOC02] ドキュメント整合性
- [Q01] 読みやすさ
- [C01] バグ検出

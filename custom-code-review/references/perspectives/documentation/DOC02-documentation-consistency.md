# ドキュメント整合性

**ID**: DOC02
**カテゴリ**: ドキュメント
**優先度**: Tier 3（オプション）
**信頼度基準**: 85-100点

---

## 参照元

- [anilcancakir/claude-code-plugins - my_docs](https://github.com/anilcancakir/claude-code-plugins)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

コードとドキュメント（README、API仕様書、設定ファイルコメント等）の整合性を確認する観点。コードが変更されたとき、関連するドキュメントが更新されないことは頻繁に発生する。

この観点では、コード変更がドキュメントに影響を与える場合、ドキュメントが適切に更新されているかをチェックする。特にAPIの変更、新機能の追加、設定項目の変更時には、ドキュメントの更新が必須となる。

---

## チェック内容

- **README更新の確認**: 新機能や設定変更がREADMEに反映されているか
- **APIドキュメントの正確性**: エンドポイント、パラメータ、レスポンス形式の一致
- **インラインドキュメントの更新**: JSDoc、PHPDoc、Pythonのdocstring等
- **設定ファイルコメントの整合性**: 環境変数、設定オプションの説明
- **変更履歴の記録**: CHANGELOG.mdやリリースノートの更新
- **コード例の動作確認**: ドキュメント内のコードサンプルが実際に動作するか

---

## 適用基準

### 使用する場合

- ✅ APIエンドポイント追加・変更
- ✅ 設定項目の追加・変更
- ✅ 新機能の追加
- ✅ 公開ライブラリのインターフェース変更
- ✅ 環境変数の追加・変更
- ✅ CLIコマンドの追加・変更

### 使用しない場合

- ❌ 内部実装のみの変更（外部に見えない）
- ❌ リファクタリングのみ（振る舞い変更なし）
- ❌ テストコードのみの変更
- ❌ バグ修正（ドキュメント影響なし）

---

## 具体例

### ❌ 悪い例1: API変更がドキュメントに反映されていない

**コード変更**:
```typescript
// 以前: function createUser(name: string)
// 変更後: function createUser(name: string, email: string)
async function createUser(name: string, email: string): Promise<User> {
  // ...
}
```

**README（未更新）**:
```markdown
## API Usage

```typescript
const user = await createUser('Alice');
```
```

**問題点**: READMEのコード例が古いままで、新しいパラメータ`email`が反映されていない。

### ❌ 悪い例2: 環境変数追加がドキュメント化されていない

**コード変更**:
```typescript
const dbTimeout = process.env.DB_TIMEOUT || 5000;
```

**README（未更新）**:
```markdown
## Environment Variables

- `DATABASE_URL`: Database connection string
- `PORT`: Server port (default: 3000)
```

**問題点**: 新しい環境変数`DB_TIMEOUT`がREADMEに記載されていない。

### ❌ 悪い例3: JSDocが実装と矛盾

**コード**:
```typescript
/**
 * ユーザーを検索する
 * @param {string} query - 検索クエリ
 * @returns {Promise<User[]>} ユーザーリスト
 */
async function searchUsers(query: string, limit: number = 10): Promise<User[]> {
  // limitパラメータが追加されたがJSDocは未更新
}
```

**問題点**: `limit`パラメータがJSDocに記載されていない。

### ✅ 良い例1: API変更とドキュメントを同時更新

**コード変更**:
```typescript
async function createUser(name: string, email: string): Promise<User> {
  // ...
}
```

**README（更新済み）**:
```markdown
## API Usage

```typescript
const user = await createUser('Alice', 'alice@example.com');
```

### Parameters

- `name`: ユーザー名（必須）
- `email`: メールアドレス（必須、v2.0.0から）
```

**理由**: コード変更と同時にREADMEも更新され、変更履歴も明記されている。

### ✅ 良い例2: 環境変数を完全にドキュメント化

**コード変更**:
```typescript
const dbTimeout = parseInt(process.env.DB_TIMEOUT || '5000', 10);
```

**README（更新済み）**:
```markdown
## Environment Variables

- `DATABASE_URL`: Database connection string
- `PORT`: Server port (default: 3000)
- `DB_TIMEOUT`: Database query timeout in milliseconds (default: 5000)
```

**理由**: 新しい環境変数が追加され、デフォルト値と単位も明記されている。

### ✅ 良い例3: JSDocを完全に更新

**コード**:
```typescript
/**
 * ユーザーを検索する
 * @param {string} query - 検索クエリ
 * @param {number} [limit=10] - 結果の最大件数（オプション）
 * @returns {Promise<User[]>} ユーザーリスト
 * @throws {Error} クエリが空の場合
 */
async function searchUsers(query: string, limit: number = 10): Promise<User[]> {
  if (!query) throw new Error('Query cannot be empty');
  // ...
}
```

**理由**: すべてのパラメータ、戻り値、例外が正確にドキュメント化されている。

---

## 関連観点

- [DOC01] コメント品質と精度
- [C02] 機能要件の適合性
- [P01] AIエージェント向け指示の遵守

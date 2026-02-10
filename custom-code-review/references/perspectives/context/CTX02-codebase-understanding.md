# コードベース理解

**ID**: CTX02
**カテゴリ**: コンテキスト分析
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- [Feature Dev Plugin - code-explorer](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Claude Code Best Practices for Local Code Review](https://fasterthanlight.me/blog/post/claude-code-best-practices-for-local-code-review)

---

## 概要

既存コードベースの深い理解に基づいてレビューを行う観点。単に変更されたコードだけを見るのではなく、エントリーポイントから出力までの実行フロー、データ変換の追跡、依存関係と統合の理解を通じて、変更が全体に与える影響を評価する。

この観点は、**変更の影響範囲**を正確に把握することに焦点を当てる。特に統合ポイントや共通関数の変更は、予期しない副作用を引き起こす可能性が高い。

---

## チェック内容

- **エントリーポイントから出力までの実行フロー**: 変更がどのように伝播するか
- **データ変換の追跡**: 入力データがどのように変換・加工されるか
- **依存関係と統合の理解**: 変更がどのモジュールに影響するか
- **状態変化と副作用の文書化**: グローバル状態やキャッシュへの影響
- **アーキテクチャレイヤーの理解**: レイヤー境界を越えた変更の妥当性
- **共通関数の影響範囲**: 複数箇所で使われる関数の変更影響
- **統合ポイントの特定**: 外部API、データベース、他サービスとの接続

---

## 適用基準

### 使用する場合

- ✅ 既存機能の変更
- ✅ 共通関数・ユーティリティの変更
- ✅ 統合ポイントの変更（外部API、データベース）
- ✅ アーキテクチャレイヤーを越えた変更
- ✅ グローバル状態の変更
- ✅ 複数モジュールに影響する変更

### 使用しない場合

- ❌ 新規ファイル作成（既存コードに影響なし）
- ❌ 完全に独立した新機能
- ❌ テストファイルのみの変更
- ❌ ドキュメント変更のみ

---

## 具体例

### ❌ 悪い例1: 共通関数の破壊的変更

**変更内容**:
```typescript
// 以前: 配列を返す
function getUsers(): User[] {
  return database.users.findAll();
}

// 変更後: Promise を返すように変更（破壊的変更）
async function getUsers(): Promise<User[]> {
  return await database.users.findAll();
}
```

**問題点**: この関数を使っている全ての箇所が影響を受けるが、変更者はそれを把握していない。

**影響範囲の例**:
```typescript
// これらのコードが全て壊れる
const users = getUsers(); // Promise<User[]> を受け取るが、配列として扱っている
users.forEach(user => console.log(user)); // エラー

// 正しくは await が必要
const users = await getUsers();
```

### ❌ 悪い例2: レイヤー境界を越えた不適切な変更

**変更内容**:
```typescript
// プレゼンテーション層から直接データベースにアクセス（レイヤー違反）
function UserProfileComponent({ userId }) {
  const user = database.users.find({ id: userId }); // ❌ レイヤー違反

  return <div>{user.name}</div>;
}
```

**問題点**: プレゼンテーション層からデータベースに直接アクセスし、アーキテクチャの分離原則に違反。

### ❌ 悪い例3: 副作用の理解不足

**変更内容**:
```typescript
// キャッシュをクリアする関数を変更
function clearUserCache(userId: string) {
  cache.delete(`user:${userId}`);
  // cache.delete(`user:${userId}:permissions`) を忘れている
}
```

**問題点**: キャッシュクリアが不完全で、権限情報が古いまま残る。副作用の全体像を理解していない。

### ✅ 良い例1: 影響範囲を確認してから変更

**変更前の確認**:
```bash
# getUsers() の使用箇所を全て確認
$ grep -r "getUsers()" src/
src/components/UserList.tsx:  const users = getUsers();
src/services/auth.ts:  const users = getUsers();
src/admin/dashboard.ts:  const allUsers = getUsers();

# 影響範囲: 3ファイル
```

**変更内容**:
```typescript
// 非同期版を新しい名前で追加（破壊的変更を避ける）
async function getUsersAsync(): Promise<User[]> {
  return await database.users.findAll();
}

// 既存の同期版は deprecation 警告付きで残す
/** @deprecated Use getUsersAsync() instead */
function getUsers(): User[] {
  return database.users.findAllSync();
}
```

**理由**: 既存のコードを壊さず、段階的に移行できるようにする。

### ✅ 良い例2: レイヤー構造を尊重

**変更内容**:
```typescript
// サービス層（ビジネスロジック）
class UserService {
  async getUser(userId: string): Promise<User> {
    return await database.users.find({ id: userId });
  }
}

// プレゼンテーション層
function UserProfileComponent({ userId }) {
  const userService = useUserService();
  const user = await userService.getUser(userId); // ✅ サービス層経由

  return <div>{user.name}</div>;
}
```

**理由**: レイヤー構造を尊重し、プレゼンテーション層はサービス層経由でデータを取得。

### ✅ 良い例3: 副作用を完全に理解

**変更内容**:
```typescript
// キャッシュの全ての関連エントリをクリア
function clearUserCache(userId: string) {
  const cacheKeys = [
    `user:${userId}`,
    `user:${userId}:permissions`,
    `user:${userId}:settings`,
    `user:${userId}:sessions`
  ];

  cacheKeys.forEach(key => cache.delete(key));

  // ログで副作用を記録
  logger.info(`Cleared all cache entries for user ${userId}`);
}
```

**理由**: ユーザーに関連する全てのキャッシュエントリを把握し、完全にクリア。

### ✅ 良い例4: データフローを追跡

**変更内容**:
```typescript
// データの変換フローを明示的に記述
async function processUserRegistration(input: UserRegistrationInput) {
  // 1. 入力検証
  const validatedInput = validateRegistrationInput(input);

  // 2. パスワードハッシュ化
  const hashedPassword = await hashPassword(validatedInput.password);

  // 3. ユーザー作成
  const user = await createUser({
    ...validatedInput,
    password: hashedPassword
  });

  // 4. ウェルカムメール送信
  await sendWelcomeEmail(user.email);

  // 5. 監査ログ記録
  await auditLog.record({
    action: 'USER_REGISTERED',
    userId: user.id
  });

  return user;
}
```

**理由**: データの変換と副作用を明示的にステップ分けし、各段階の責任を明確化。

### ✅ 良い例5: 統合ポイントの影響を確認

**変更内容**:
```typescript
// 外部APIのレスポンス形式が変わる場合
interface OldApiResponse {
  user_id: string;
  user_name: string;
}

interface NewApiResponse {
  id: string;         // user_id → id に変更
  name: string;       // user_name → name に変更
  email?: string;     // 新フィールド
}

// アダプタパターンで既存コードを保護
function adaptApiResponse(response: NewApiResponse): OldApiResponse {
  return {
    user_id: response.id,
    user_name: response.name
  };
}

// 既存コードは変更不要
const oldFormat = adaptApiResponse(newApiResponse);
```

**理由**: 外部APIの変更を吸収するアダプタを作成し、既存コードへの影響を最小化。

---

## 関連観点

- [CTX01] Git履歴分析
- [D02] アーキテクチャパターン準拠
- [D04] 依存関係管理
- [D05] データフロー設計
- [S08] ブラストラジアス（影響範囲）分析

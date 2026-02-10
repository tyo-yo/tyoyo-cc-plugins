# エラーハンドリング品質

**ID**: T03
**カテゴリ**: テストとエラー処理
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)

---

## 概要

エラーハンドリング品質は、エラー処理の適切性を評価します。エラーが適切にログ記録され、ユーザーに明確なフィードバックが提供され、必要に応じてエスカレーションされるかを確認します。

重要なのは、エラーが「サイレント」に失敗せず、適切なログレベル、充分なコンテキスト情報、実行可能な対応策が含まれることです。

---

## チェック内容

- 適切なログレベルの使用
  - ERROR: システムエラー、例外
  - WARN: 回復可能だが注意が必要
  - INFO: 通常動作の重要イベント
  - DEBUG: デバッグ情報
- 充分なコンテキスト情報
  - エラーメッセージ
  - スタックトレース
  - 入力パラメータ
  - ユーザーID、リクエストID
  - タイムスタンプ
- エラーIDの付与
  - 一意なエラー識別子
  - サポート問い合わせに使用可能
- ユーザーへの明確なフィードバック
  - 何が起きたか
  - なぜ起きたか
  - 何をすべきか
- 実行可能な対応策の提示
  - 具体的なアクション（再試行、入力修正等）
  - サポート連絡先
- 技術詳細の適切な露出
  - ユーザー向け: シンプルなメッセージ
  - ログ向け: 詳細な技術情報
- キャッチの特異性（広すぎないか）
  - 特定の例外型をキャッチ
  - `catch (error)` の乱用を避ける
- エラー伝播の適切性
  - 適切なレイヤーで処理
  - 必要に応じて再スロー

---

## 適用基準

### 使用する場合

- ✅ エラーハンドリング追加・変更
- ✅ Try-catchブロックを含む
- ✅ エラーログ処理変更

### 使用しない場合

- ❌ エラーハンドリングに関係しないコード変更

---

## 具体例

### ❌ 悪い例

```typescript
try {
  const result = await fetchUserData(userId);
  return result;
} catch (error) {
  // 広すぎるキャッチ、コンテキスト不足
  console.log('Error occurred');
  return null; // サイレントフェイラー
}

// エラー情報が不足
throw new Error('Invalid input');

// 技術詳細をユーザーに露出
res.status(500).json({
  error: 'Database connection failed: Connection timeout at line 42'
});
```

**問題点**: 広すぎる例外捕捉、コンテキスト不足、サイレントフェイラー、技術詳細の不適切な露出。

### ✅ 良い例

```typescript
try {
  const result = await fetchUserData(userId);
  return result;
} catch (error) {
  if (error instanceof NetworkError) {
    // 特異的なエラーハンドリング
    logger.error('Failed to fetch user data', {
      errorId: generateErrorId(),
      userId,
      errorType: error.name,
      message: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    });

    // ユーザーへの明確なフィードバック
    throw new UserFacingError(
      'ユーザー情報の取得に失敗しました。',
      {
        errorCode: 'USER_FETCH_FAILED',
        action: 'しばらく待ってから再度お試しください。',
        supportContact: 'support@example.com'
      }
    );
  }

  if (error instanceof ValidationError) {
    logger.warn('Invalid user ID provided', {
      userId,
      errorType: error.name,
      message: error.message
    });

    throw new UserFacingError(
      '無効なユーザーIDです。',
      {
        errorCode: 'INVALID_USER_ID',
        action: 'ユーザーIDを確認してください。'
      }
    );
  }

  // 予期しないエラーは再スロー
  logger.error('Unexpected error in fetchUserData', {
    errorId: generateErrorId(),
    userId,
    error: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : undefined
  });
  throw error;
}

// 充分なコンテキスト情報
if (!isValidEmail(email)) {
  throw new ValidationError(
    `Invalid email format: ${email}`,
    {
      field: 'email',
      value: email,
      constraint: 'Must be valid email format'
    }
  );
}

// ユーザー向けと内部ログの分離
res.status(500).json({
  error: 'サーバーエラーが発生しました。',
  errorCode: 'DB_CONNECTION_FAILED',
  action: 'しばらく待ってから再度お試しください。',
  errorId: 'ERR-2026-02-11-1234'
});

logger.error('Database connection failed', {
  errorId: 'ERR-2026-02-11-1234',
  details: 'Connection timeout at line 42',
  connectionString: sanitizeConnectionString(config.dbUrl),
  retryCount: 3
});
```

**理由**: 特異的な例外処理、充分なコンテキスト、ユーザー向けメッセージと内部ログの分離、実行可能な対応策。

---

## 関連観点

- [C04] サイレントフェイラー
- [T01] テストカバレッジ
- [C05] 例外安全性

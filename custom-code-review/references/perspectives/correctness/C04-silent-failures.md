# サイレントフェイラー

**ID**: C04
**カテゴリ**: 正確性（基本）
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点

---

## 参照元

- [PR Review Toolkit - Silent Failure Hunter](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)

---

## 概要

この観点は、エラーが適切に伝播・通知されるかを確認します。「サイレントフェイラー」とは、エラーが発生しているにもかかわらず、それが隠蔽され、システムやユーザーに通知されない状態を指します。

エラーハンドリングの追加・変更、try-catchブロックを含むコード、ログ処理変更の際に適用し、致命的なエラーが隠蔽されることを防ぎます。

---

## チェック内容

- 空のcatchブロック
  - 例外を捕捉するが何もしない
  - コメントのみで実際の処理がない
- エラーをログのみで吸収
  - エラーをログに記録するが処理を続行
  - 呼び出し元に通知しない
- 無言でデフォルト値を返す
  - エラー時に警告なくデフォルト値を返す
  - 失敗したことをユーザーが知らない
- 不適切なフォールバック動作
  - エラー時の代替動作が不適切
  - 部分的な成功を完全な成功として扱う
- ユーザーへのフィードバック欠如
  - エラーメッセージが表示されない
  - 失敗理由が不明
- 広すぎる例外捕捉（catch-all）
  - すべての例外を一律に処理
  - 異なるエラーの区別がない
- 本番コードのモック実装
  - デバッグ用のダミー実装が残留
  - 常に成功を返すスタブコード
- 説明なしの再試行
  - 失敗を隠して自動的に再試行
  - リトライ回数の制限がない

---

## 適用基準

### 使用する場合

- ✅ エラーハンドリング追加・変更
- ✅ Try-catchブロックを含むコード
- ✅ ログ処理変更
- ✅ 外部API呼び出し
- ✅ データベース操作
- ✅ ファイル操作

### 使用しない場合

- ❌ エラー処理を含まないコード

---

## 具体例

### ❌ 悪い例：空のcatchブロック

```python
def save_user_data(user_id, data):
    try:
        database.update(user_id, data)
    except Exception:
        pass  # 問題: エラーが完全に無視される
```

**問題点**: データベースの更新が失敗してもエラーが完全に隠蔽され、呼び出し元やユーザーに通知されません。データ損失のリスクがあります。

### ✅ 良い例

```python
def save_user_data(user_id, data):
    try:
        database.update(user_id, data)
    except DatabaseConnectionError as e:
        logger.error(f"Database connection failed: {e}", extra={"user_id": user_id})
        raise ServiceUnavailableError("Failed to save user data. Please try again later.") from e
    except Exception as e:
        logger.error(f"Unexpected error saving user data: {e}", extra={"user_id": user_id})
        raise
```

**理由**: エラーをログに記録し、適切な例外として呼び出し元に伝播させています。

---

### ❌ 悪い例：エラーをログのみで吸収

```typescript
async function sendEmail(to: string, subject: string, body: string): Promise<void> {
  try {
    await emailService.send({ to, subject, body });
  } catch (error) {
    // 問題: ログに記録するが、呼び出し元に通知しない
    logger.error('Failed to send email', { error, to, subject });
    // 処理は続行される
  }
}

// 呼び出し側
await sendEmail(user.email, 'Welcome', 'Welcome to our service!');
// ユーザーは「メール送信成功」と思っているが、実際には失敗している
```

**問題点**: メール送信が失敗してもエラーが呼び出し元に伝播せず、ユーザーは成功したと誤認します。

### ✅ 良い例

```typescript
async function sendEmail(to: string, subject: string, body: string): Promise<void> {
  try {
    await emailService.send({ to, subject, body });
  } catch (error) {
    logger.error('Failed to send email', { error, to, subject });
    throw new EmailSendError(`Failed to send email to ${to}`, { cause: error });
  }
}

// 呼び出し側
try {
  await sendEmail(user.email, 'Welcome', 'Welcome to our service!');
  showSuccessMessage('Welcome email sent successfully!');
} catch (error) {
  showErrorMessage('Failed to send welcome email. Please check your email address.');
}
```

**理由**: エラーを適切に伝播させ、呼び出し元で適切なユーザーフィードバックを提供できます。

---

### ❌ 悪い例：無言でデフォルト値を返す

```javascript
function getUserSettings(userId) {
  try {
    return database.getSettings(userId);
  } catch (error) {
    // 問題: エラーを隠してデフォルト値を返す
    return { theme: 'light', language: 'en' };
  }
}
```

**問題点**: データベースの接続エラーが発生してもユーザーには通知されず、デフォルト設定が表示されます。ユーザーは自分の設定が失われたと誤解する可能性があります。

### ✅ 良い例

```javascript
function getUserSettings(userId) {
  try {
    return database.getSettings(userId);
  } catch (error) {
    logger.error('Failed to load user settings', { userId, error });

    // 一時的なエラーの場合は通知
    if (error instanceof TemporaryDatabaseError) {
      throw new Error('Unable to load your settings. Please try again in a moment.');
    }

    // ユーザーが設定を保存していない場合のみデフォルト値
    if (error instanceof NotFoundError) {
      return { theme: 'light', language: 'en' };
    }

    throw error;
  }
}
```

**理由**: エラーの種類に応じて適切に処理し、ユーザーに状況を通知します。

---

### ❌ 悪い例：広すぎる例外捕捉

```python
def process_payment(order_id, amount):
    try:
        validate_order(order_id)
        charge_card(amount)
        update_order_status(order_id, "paid")
        send_confirmation_email(order_id)
    except Exception as e:
        # 問題: すべてのエラーを同じように処理
        logger.error(f"Payment processing failed: {e}")
        return {"success": False, "error": "Payment failed"}
```

**問題点**: バリデーションエラー、決済エラー、メール送信エラーをすべて同じように扱い、適切な対応ができません。

### ✅ 良い例

```python
def process_payment(order_id, amount):
    try:
        validate_order(order_id)
    except ValidationError as e:
        logger.warning(f"Invalid order: {e}", extra={"order_id": order_id})
        raise BadRequestError(f"Invalid order: {str(e)}") from e

    try:
        charge_card(amount)
    except PaymentGatewayError as e:
        logger.error(f"Payment gateway error: {e}", extra={"order_id": order_id, "amount": amount})
        raise PaymentFailedError("Payment processing failed. Your card was not charged.") from e

    try:
        update_order_status(order_id, "paid")
    except DatabaseError as e:
        # 決済は成功したが注文ステータスの更新に失敗
        logger.critical(f"Order status update failed after successful payment: {e}",
                       extra={"order_id": order_id})
        # 人手介入が必要
        raise CriticalError("Payment successful but order status update failed. Support will contact you.") from e

    try:
        send_confirmation_email(order_id)
    except EmailError as e:
        # メール送信失敗は致命的ではない
        logger.warning(f"Confirmation email failed: {e}", extra={"order_id": order_id})
        # エラーは伝播させない（決済は成功しているため）

    return {"success": True, "order_id": order_id}
```

**理由**: エラーの種類ごとに適切な処理を行い、重要度に応じて伝播を制御しています。

---

### ❌ 悪い例：本番コードのモック実装

```typescript
function authenticateUser(username: string, password: string): boolean {
  // TODO: Implement actual authentication
  // 問題: 常に true を返すモック実装が本番に残っている
  return true;
}
```

**問題点**: 認証が常に成功するため、セキュリティ上の重大な脆弱性になります。

### ✅ 良い例

```typescript
function authenticateUser(username: string, password: string): boolean {
  const user = database.getUserByUsername(username);

  if (!user) {
    return false;
  }

  return bcrypt.compareSync(password, user.passwordHash);
}
```

**理由**: 実際の認証ロジックが実装されています。

---

## 2026年トレンド

AI生成コードでは、エラーハンドリングブロックは生成されるものの、適切なエラー伝播やユーザー通知が欠けていることが多いです。特に「空のcatchブロック」や「ログのみで吸収」パターンに注意が必要です。

---

## 関連観点

- [C01] バグ検出
- [C03] エッジケースとバウンダリー条件
- [T03] エラーハンドリング品質
- [S01] セキュリティ脆弱性（基本）

# E2Eテスト計画

**ID**: T05
**カテゴリ**: テストとエラー処理
**優先度**: Tier 3（オプション）
**信頼度基準**: 80-100点

---

## 参照元

- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)

---

## 概要

E2E（End-to-End）テスト計画は、ユーザーフローや統合機能の追加時に、システム全体の動作を検証するテストが計画されているかを確認します。

ユニットテストや統合テストでは検出できない、実際のユーザー操作やシステム間連携の問題を発見するために重要です。ただし、実行コストが高いため、Tier 3（オプション）として、重要なユーザーフローや統合機能の変更時のみ適用します。

---

## チェック内容

- ユーザーフローのE2Eテスト計画
  - ログイン → 操作 → ログアウト
  - データ作成 → 編集 → 削除
  - 購入フロー、決済フロー
- 統合機能のE2Eテスト計画
  - 外部API連携
  - データベース操作
  - ファイルシステム操作
  - メール送信、通知
- 重要なユーザーストーリーのカバー
  - ビジネスクリティカルな機能
  - 高頻度で使用される機能
- エラーシナリオのE2Eテスト
  - ネットワークエラー時の動作
  - タイムアウト時の動作
  - 認証失敗時の動作
- クロスブラウザテスト（Web開発）
  - Chrome、Firefox、Safari、Edge
  - モバイルブラウザ

---

## 適用基準

### 使用する場合

- ✅ ユーザーフロー変更（ログイン、購入等）
- ✅ 統合機能追加（外部API、DB連携等）
- ✅ ビジネスクリティカルな機能変更

### 使用しない場合

- ❌ 内部ロジック変更のみ（ユーザーフロー影響なし）
- ❌ ドキュメント変更のみ
- ❌ スタイル変更のみ

---

## 具体例

### ❌ 悪い例

```typescript
// ユーザー登録フローの変更
// 新機能: メール認証を追加
async function registerUser(email: string, password: string) {
  const user = await createUser(email, password);
  await sendVerificationEmail(user.email);
  return user;
}

// ユニットテストのみ（E2Eテストなし）
test('creates user', async () => {
  const user = await registerUser('test@example.com', 'password123');
  expect(user.email).toBe('test@example.com');
});

test('sends verification email', async () => {
  jest.spyOn(emailService, 'send');
  await registerUser('test@example.com', 'password123');
  expect(emailService.send).toHaveBeenCalled();
});
```

**問題点**: ユニットテストはあるが、実際のユーザーフロー（登録 → メール受信 → 認証リンククリック → ログイン）のE2Eテストがない。

### ✅ 良い例

```typescript
// ユーザー登録フローの変更
// 新機能: メール認証を追加
async function registerUser(email: string, password: string) {
  const user = await createUser(email, password);
  await sendVerificationEmail(user.email);
  return user;
}

// ユニットテスト
test('creates user', async () => {
  const user = await registerUser('test@example.com', 'password123');
  expect(user.email).toBe('test@example.com');
});

// E2Eテスト計画（Playwright, Cypress等）
describe('User Registration Flow (E2E)', () => {
  test('complete registration with email verification', async ({ page }) => {
    // 1. 登録ページを開く
    await page.goto('/register');

    // 2. フォームに入力
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // 3. 確認メッセージを確認
    await expect(page.locator('.success-message')).toContainText(
      '確認メールを送信しました'
    );

    // 4. メールボックスから認証リンクを取得（テスト用APIで取得）
    const verificationLink = await getLatestEmailLink('test@example.com');

    // 5. 認証リンクをクリック
    await page.goto(verificationLink);

    // 6. 認証完了メッセージを確認
    await expect(page.locator('.verification-success')).toContainText(
      'メール認証が完了しました'
    );

    // 7. ログイン
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // 8. ダッシュボードにリダイレクトされることを確認
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.welcome-message')).toContainText('ようこそ');
  });

  test('error: registration with unverified email cannot login', async ({ page }) => {
    // 1. 登録（認証メールは送信されるがクリックしない）
    await page.goto('/register');
    await page.fill('input[name="email"]', 'unverified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // 2. ログイン試行
    await page.goto('/login');
    await page.fill('input[name="email"]', 'unverified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // 3. エラーメッセージを確認
    await expect(page.locator('.error-message')).toContainText(
      'メール認証が完了していません'
    );
  });
});
```

**理由**: ユーザーフロー全体（登録 → メール認証 → ログイン）をE2Eテストでカバーし、エラーシナリオも含む。

---

## E2Eテストのベストプラクティス

- **テストの独立性**: 各テストで独立したユーザーデータを使用
- **テストデータのクリーンアップ**: テスト後にデータベースをクリーンアップ
- **外部サービスのモック**: 本番APIを叩かない（テスト用API使用）
- **ウェイト戦略**: `page.waitForLoadState()` を使用（固定sleepは避ける）
- **スクリーンショット**: テスト失敗時にスクリーンショットを保存

---

## 関連観点

- [T01] テストカバレッジ
- [C02] 機能要件の適合性
- [D05] データフロー設計

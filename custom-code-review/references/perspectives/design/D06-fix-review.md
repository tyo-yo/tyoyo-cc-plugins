# 修正の検証（Fix Review）

**ID**: D06
**カテゴリ**: 設計とアーキテクチャ
**優先度**: Tier 3（オプション）
**信頼度基準**: 80-100点

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

バグ修正PRは、単に「動くようになった」だけでなく、根本原因が解決され、同様の問題が再発しない設計になっているかを検証する必要があります。本観点では、修正の適切性、根本原因の分析、回帰テストの追加、同様の問題の潜在箇所を評価します。

---

## チェック内容

- 修正の適切性
  - 根本原因を解決しているか（表面的な対処ではないか）
  - 最小限の変更で問題を解決しているか
  - 副作用を生んでいないか
- 根本原因の分析
  - なぜバグが発生したかの分析
  - 設計上の問題の特定
  - 同様の問題が他の箇所にないかの確認
- 回帰テストの追加
  - バグを再現するテストケースの追加
  - エッジケースのカバー
  - 将来の回帰を防ぐテスト
- ドキュメント更新
  - 修正内容の記録
  - なぜこの修正が必要だったかの説明
  - 今後の注意点の記載

---

## 適用基準

### 使用する場合

- ✅ バグ修正PR
- ✅ セキュリティ脆弱性修正
- ✅ パフォーマンス問題修正
- ✅ データ不整合の修正

### 使用しない場合

- ❌ 新機能追加
- ❌ リファクタリングのみ
- ❌ ドキュメント変更のみ

---

## 具体例

### ❌ 悪い例: 表面的な対処

```python
def calculate_average(numbers):
    # バグ報告: 空のリストで ZeroDivisionError が発生
    # 修正: エラーを握りつぶす（表面的）
    try:
        return sum(numbers) / len(numbers)
    except ZeroDivisionError:
        return 0  # 0を返すのは適切か?
```

**問題点**: エラーを握りつぶしているだけで、根本原因（空リストの扱い）を解決していません。

### ✅ 良い例: 根本原因の解決とテスト追加

```python
def calculate_average(numbers: list[float]) -> float:
    """
    数値リストの平均を計算します。

    Args:
        numbers: 数値のリスト（空でない必要があります）

    Returns:
        平均値

    Raises:
        ValueError: リストが空の場合
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    return sum(numbers) / len(numbers)

# 回帰テスト追加
def test_calculate_average():
    # 正常系
    assert calculate_average([1, 2, 3]) == 2.0

    # バグを再現するテストケース
    with pytest.raises(ValueError, match="empty list"):
        calculate_average([])

    # エッジケース
    assert calculate_average([5]) == 5.0
    assert calculate_average([1.5, 2.5]) == 2.0
```

**理由**: 空リストの扱いを明確にし、例外を適切に発生させ、テストで将来の回帰を防いでいます。

---

### ❌ 悪い例: 根本原因を見逃す

```javascript
// バグ報告: ユーザーがログアウトしても前のユーザーのデータが残る
function logout() {
  // 修正: ローカルストレージをクリア
  localStorage.removeItem('authToken');
  // ここだけの修正では不十分
}

// 他の箇所でグローバル変数を使用（見逃されている）
let currentUser = null;

function login(user) {
  currentUser = user;
  localStorage.setItem('authToken', user.token);
}

function getUserData() {
  // currentUserがクリアされていない（バグの根本原因）
  return currentUser;
}
```

**問題点**: ローカルストレージのクリアだけでは不十分で、グローバル変数`currentUser`がクリアされていません。

### ✅ 良い例: 根本原因の完全な解決

```javascript
// セッション管理を一元化
class UserSession {
  private currentUser: User | null = null;
  private authToken: string | null = null;

  login(user: User): void {
    this.currentUser = user;
    this.authToken = user.token;
    localStorage.setItem('authToken', user.token);
  }

  logout(): void {
    // すべての状態をクリア
    this.currentUser = null;
    this.authToken = null;
    localStorage.removeItem('authToken');

    // セッションストレージもクリア（念のため）
    sessionStorage.clear();
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }
}

// テスト追加
describe('UserSession', () => {
  it('should clear all user data on logout', () => {
    const session = new UserSession();
    const user = { id: '123', name: 'Alice', token: 'abc' };

    session.login(user);
    expect(session.getCurrentUser()).toEqual(user);
    expect(localStorage.getItem('authToken')).toBe('abc');

    session.logout();

    // バグを再現するテスト: すべての状態がクリアされる
    expect(session.getCurrentUser()).toBeNull();
    expect(localStorage.getItem('authToken')).toBeNull();
  });
});
```

**理由**: セッション管理を一元化し、すべての状態を確実にクリアし、テストで検証しています。

---

### ❌ 悪い例: 同様の問題を見逃す

```python
# バグ修正: order_service.py で注文キャンセル時に在庫が戻らない
class OrderService:
    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        order.status = 'cancelled'
        # 修正: 在庫を戻す
        for item in order.items:
            self.inventory.increase_stock(item.product_id, item.quantity)
        self.save(order)

# 同様の問題が他の箇所にも存在（見逃されている）
class RefundService:
    def process_refund(self, order_id):
        order = self.get_order(order_id)
        payment.refund(order.amount)
        order.status = 'refunded'
        # ここでも在庫を戻すべき（見逃されている）
        self.save(order)
```

**問題点**: 同じパターンの問題が他のサービスにも存在しています。

### ✅ 良い例: 同様の問題の網羅的修正

```python
# 在庫管理を共通化
class InventoryManager:
    def restore_stock(self, order: Order, reason: str):
        """
        注文に含まれる商品の在庫を戻します。

        Args:
            order: 対象の注文
            reason: 在庫を戻す理由（ログ用）
        """
        logger.info(f"Restoring stock for order {order.id}: {reason}")

        for item in order.items:
            self.increase_stock(item.product_id, item.quantity)
            logger.info(
                f"Restored {item.quantity} units of product {item.product_id}"
            )

class OrderService:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager

    def cancel_order(self, order_id: str):
        order = self.get_order(order_id)
        order.status = 'cancelled'
        # 共通処理を使用
        self.inventory.restore_stock(order, 'order cancelled')
        self.save(order)

class RefundService:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager

    def process_refund(self, order_id: str):
        order = self.get_order(order_id)
        payment.refund(order.amount)
        order.status = 'refunded'
        # 同じ共通処理を使用
        self.inventory.restore_stock(order, 'refund processed')
        self.save(order)

# 包括的なテスト
def test_stock_restoration():
    """在庫復元が必要なすべてのシナリオをテスト"""

    # キャンセル時
    order_service.cancel_order('123')
    assert inventory.get_stock('product1') == 100

    # 返金時
    refund_service.process_refund('456')
    assert inventory.get_stock('product2') == 200
```

**理由**: 在庫復元を共通処理として抽出し、すべての箇所で一貫して使用し、包括的なテストで検証しています。

---

### ❌ 悪い例: 回帰テストの欠如

```java
// バグ修正: 日付パースでタイムゾーンが考慮されていない
public Date parseDate(String dateString) {
    // 修正: タイムゾーンを考慮
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
    return formatter.parse(dateString);
}

// テストなし（回帰リスク）
```

**問題点**: 修正は行われたが、回帰テストが追加されていません。

### ✅ 良い例: 回帰テストの追加

```java
public Date parseDate(String dateString) {
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
    return formatter.parse(dateString);
}

// 回帰テスト追加
@Test
public void testParseDateWithTimezone() {
    // バグを再現するテストケース
    String dateString = "2026-02-10 12:00:00";
    Date parsed = parseDate(dateString);

    // UTCとして解釈されることを検証
    Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
    cal.setTime(parsed);
    assertEquals(2026, cal.get(Calendar.YEAR));
    assertEquals(1, cal.get(Calendar.MONTH)); // 0-indexed
    assertEquals(10, cal.get(Calendar.DAY_OF_MONTH));
    assertEquals(12, cal.get(Calendar.HOUR_OF_DAY));
}

@Test
public void testParseDateConsistency() {
    // タイムゾーンの異なる環境でも一貫した結果
    TimeZone originalTz = TimeZone.getDefault();
    try {
        TimeZone.setDefault(TimeZone.getTimeZone("Asia/Tokyo"));
        Date parsed1 = parseDate("2026-02-10 12:00:00");

        TimeZone.setDefault(TimeZone.getTimeZone("America/New_York"));
        Date parsed2 = parseDate("2026-02-10 12:00:00");

        assertEquals(parsed1, parsed2);
    } finally {
        TimeZone.setDefault(originalTz);
    }
}
```

**理由**: バグを再現するテストケースと、将来の回帰を防ぐ包括的なテストを追加しています。

---

## 2026年トレンド

バグ修正レビューにおいて以下のトレンドが見られます。

- AIによる類似バグの自動検出
- Git Blameによる変更履歴分析
- Mutation Testing（変異テスト）による修正の検証
- Chaos Engineering（カオスエンジニアリング）による堅牢性検証
- Post-Mortem（事後分析）の標準化

AI生成の修正コードは、表面的な対処に留まることが多いため、根本原因の分析と包括的なテストが特に重要です。

---

## 関連観点

- [C01] バグ検出
- [T04] リグレッションテスト
- [CTX01] Git履歴分析
- [D02] アーキテクチャパターン準拠

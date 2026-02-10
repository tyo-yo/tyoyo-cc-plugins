# 例外安全性

**ID**: C05
**カテゴリ**: 正確性（基本）
**優先度**: Tier 2（推奨）
**信頼度基準**: 85-100点

---

## 参照元

- 新規観点（ベストプラクティスより）

---

## 概要

この観点は、例外が発生した場合でもプログラムが安全な状態を保つことを確認します。リソースリークの回避、トランザクションの整合性、状態の一貫性維持など、例外が発生しても問題が起きないコードを実現します。

リソース管理コード、トランザクション処理、ファイル/データベース操作の際に適用し、例外発生時の安全性を保証します。

---

## チェック内容

- リソースリークの回避
  - ファイルハンドルの確実なクローズ（finally/defer/RAII）
  - データベース接続のクローズ
  - ネットワークソケットのクローズ
  - メモリの解放
- トランザクションの整合性
  - ロールバックの実装
  - コミット失敗時の処理
  - 部分的な成功の防止
- 状態の一貫性維持
  - 例外発生前の状態に戻す
  - 不変条件（invariant）の維持
  - 中途半端な状態の回避
- 例外中立性
  - 例外を適切に伝播
  - 情報を失わない再スロー
  - 適切な例外変換
- 適切な例外型の選択
  - カスタム例外クラスの使用
  - 例外階層の設計
  - チェック例外vs非チェック例外

---

## 適用基準

### 使用する場合

- ✅ リソース管理コード（ファイル、DB、ネットワーク）
- ✅ トランザクション処理
- ✅ ファイル操作
- ✅ データベース操作
- ✅ 複数ステップの操作

### 使用しない場合

- ❌ リソース管理を含まないシンプルな関数
- ❌ 純粋関数（副作用なし）

---

## 具体例

### ❌ 悪い例：リソースリーク

```python
def read_config(filename):
    file = open(filename, 'r')
    data = json.load(file)
    # 問題: 例外が発生した場合、ファイルがクローズされない
    process_config(data)  # この行で例外が発生する可能性
    file.close()
    return data
```

**問題点**: `process_config(data)`で例外が発生すると、`file.close()`が実行されずファイルハンドルがリークします。

### ✅ 良い例

```python
def read_config(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        process_config(data)
        return data
    # ファイルは例外が発生しても確実にクローズされる
```

**理由**: `with`文を使用することで、例外の有無に関わらずファイルが確実にクローズされます。

---

### ❌ 悪い例：トランザクションの不整合

```typescript
async function transferMoney(fromAccount: string, toAccount: string, amount: number) {
  await debitAccount(fromAccount, amount);
  // 問題: この間に例外が発生すると、お金が消える
  await creditAccount(toAccount, amount);
}
```

**問題点**: `debitAccount`が成功した後、`creditAccount`の前に例外が発生すると、送金元からお金が引かれたまま送金先に入らず、資金が消失します。

### ✅ 良い例

```typescript
async function transferMoney(fromAccount: string, toAccount: string, amount: number) {
  const transaction = await database.beginTransaction();

  try {
    await debitAccount(fromAccount, amount, transaction);
    await creditAccount(toAccount, amount, transaction);
    await transaction.commit();
  } catch (error) {
    await transaction.rollback();
    logger.error('Transfer failed, rolled back', { fromAccount, toAccount, amount, error });
    throw new TransferError('Money transfer failed. No funds were moved.', { cause: error });
  }
}
```

**理由**: トランザクションを使用し、例外発生時には確実にロールバックされます。

---

### ❌ 悪い例：状態の不整合

```javascript
class ShoppingCart {
  constructor() {
    this.items = [];
    this.total = 0;
  }

  addItem(item) {
    this.items.push(item);
    // 問題: この間に例外が発生すると、itemsとtotalが不整合になる
    this.total += item.price;
  }
}
```

**問題点**: `this.total += item.price`で例外が発生すると、itemsには追加されたがtotalは更新されない不整合な状態になります。

### ✅ 良い例

```javascript
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    if (!item || typeof item.price !== 'number') {
      throw new Error('Invalid item');
    }
    this.items.push(item);
  }

  get total() {
    // 常に items から計算するため、不整合が発生しない
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

**理由**: `total`を保存せず常に計算することで、状態の不整合を防ぎます。

---

### ❌ 悪い例：不適切な例外の飲み込み

```python
def save_document(doc_id, content):
    try:
        document = get_document(doc_id)
        document.content = content
        document.save()
    except Exception:
        # 問題: すべての例外を無視して空のドキュメントを返す
        return Document(id=doc_id, content="")
```

**問題点**: データベースエラー、ネットワークエラーなどすべての例外を無視し、空のドキュメントを返すことで問題を隠蔽します。

### ✅ 良い例

```python
def save_document(doc_id, content):
    try:
        document = get_document(doc_id)
        document.content = content
        document.save()
        return document
    except DocumentNotFoundError as e:
        logger.warning(f"Document not found: {doc_id}")
        raise
    except DatabaseError as e:
        logger.error(f"Failed to save document: {doc_id}", extra={"error": str(e)})
        raise DocumentSaveError(f"Failed to save document {doc_id}") from e
```

**理由**: 例外の種類に応じて適切に処理し、情報を失わずに伝播させます。

---

### ❌ 悪い例：例外安全性のないクリーンアップ

```typescript
async function processFile(filename: string) {
  const tempFile = await createTempFile();

  try {
    const data = await readFile(filename);
    await writeFile(tempFile, processData(data));
    await moveFile(tempFile, filename);
  } finally {
    // 問題: moveFile が成功した後は tempFile は存在しない
    await deleteFile(tempFile);  // エラーになる
  }
}
```

**問題点**: `moveFile`が成功すると`tempFile`は存在しなくなるため、`deleteFile`でエラーが発生します。

### ✅ 良い例

```typescript
async function processFile(filename: string) {
  const tempFile = await createTempFile();
  let tempFileExists = true;

  try {
    const data = await readFile(filename);
    await writeFile(tempFile, processData(data));
    await moveFile(tempFile, filename);
    tempFileExists = false;  // 移動成功、tempFileは存在しない
  } finally {
    if (tempFileExists) {
      try {
        await deleteFile(tempFile);
      } catch (error) {
        logger.warning('Failed to delete temp file', { tempFile, error });
        // クリーンアップの失敗は致命的ではない
      }
    }
  }
}
```

**理由**: 一時ファイルの存在を追跡し、存在する場合のみ削除を試みます。また、クリーンアップの失敗は警告のみにとどめます。

---

### ❌ 悪い例：複数リソースの不適切な管理

```java
public void processData(String inputFile, String outputFile) throws IOException {
    FileInputStream input = new FileInputStream(inputFile);
    FileOutputStream output = new FileOutputStream(outputFile);

    // 問題: output のオープンで例外が発生すると input がクローズされない
    byte[] buffer = new byte[1024];
    int length;
    while ((length = input.read(buffer)) > 0) {
        output.write(buffer, 0, length);
    }

    input.close();
    output.close();
}
```

**問題点**: `FileOutputStream`のコンストラクタで例外が発生すると、`input`がクローズされません。

### ✅ 良い例

```java
public void processData(String inputFile, String outputFile) throws IOException {
    try (FileInputStream input = new FileInputStream(inputFile);
         FileOutputStream output = new FileOutputStream(outputFile)) {

        byte[] buffer = new byte[1024];
        int length;
        while ((length = input.read(buffer)) > 0) {
            output.write(buffer, 0, length);
        }
    }
    // try-with-resources により、例外の有無に関わらず両方のストリームがクローズされる
}
```

**理由**: try-with-resourcesを使用し、複数のリソースを安全に管理しています。

---

## 関連観点

- [C01] バグ検出
- [C04] サイレントフェイラー
- [PERF03] リソース管理

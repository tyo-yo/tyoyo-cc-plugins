# リソース管理

**ID**: PERF03
**カテゴリ**: パフォーマンス
**優先度**: Tier 2（推奨）
**信頼度基準**: 91-100点（確実）、80-90点（潜在的）

---

## 参照元

- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)
- [Edge Cases and Error Handling: Where AI Code Falls Short](https://codefix.dev/2026/02/02/ai-coding-edge-case-fix/)

---

## 概要

ファイル、データベース接続、メモリ、タイマー、イベントリスナー等のリソースが適切に管理されているかを確認する観点。リソースの取得と解放が正しくペアになっていないと、リソースリークが発生し、長時間稼働するアプリケーションでメモリ不足やファイルハンドル枯渇を引き起こす。

AIツールは「動作するコード」を生成するが、リソースのクリーンアップを忘れることが多い。この観点では、特に例外発生時やエラー時のリソース解放を重点的にチェックする。

---

## チェック内容

- **ファイルハンドルのクローズ**: ファイル操作後の確実なクローズ
- **データベース接続のクローズ**: 接続プール管理の適切性
- **メモリリークの回避**: 不要なオブジェクトへの参照保持
- **タイマーのクリーンアップ**: `setInterval`、`setTimeout`の適切な解除
- **イベントリスナーの解除**: DOMイベントやカスタムイベントの登録解除
- **ストリームのクローズ**: 読み込み/書き込みストリームの終了処理
- **WebSocketやHTTP接続の終了**: 長時間接続のクローズ
- **例外発生時のクリーンアップ**: finally句やRAIIパターンの使用

---

## 適用基準

### 使用する場合

- ✅ ファイル操作（読み込み、書き込み）
- ✅ データベース操作
- ✅ ネットワーク接続（HTTP、WebSocket、gRPC）
- ✅ タイマー処理（`setInterval`、`setTimeout`）
- ✅ イベントリスナー登録
- ✅ リソース集約的な処理
- ✅ 長時間稼働するアプリケーション

### 使用しない場合

- ❌ 単純な計算処理
- ❌ 短命なスクリプト（起動して終了）
- ❌ リソースを使用しないロジック
- ❌ ガベージコレクタが自動管理するメモリ（通常のオブジェクト）

---

## 具体例

### ❌ 悪い例1: ファイルハンドルがクローズされない

```javascript
// リソースリークの危険性
function readConfig(filePath) {
  const fs = require('fs');
  const fd = fs.openSync(filePath, 'r');
  const buffer = Buffer.alloc(1024);

  fs.readSync(fd, buffer, 0, 1024, 0);
  // fs.closeSync(fd) を忘れている！

  return buffer.toString();
}
```

**問題点**: ファイルディスクリプタがクローズされず、繰り返し呼ばれるとファイルハンドル枯渇が発生。

### ❌ 悪い例2: イベントリスナーが解除されない

```javascript
// メモリリークの危険性
function setupListener() {
  const button = document.querySelector('#myButton');

  button.addEventListener('click', () => {
    console.log('Button clicked');
  });

  // removeEventListener を忘れている
  // コンポーネントが破棄されてもリスナーが残る
}
```

**問題点**: コンポーネントが破棄されてもイベントリスナーが残り、メモリリークの原因となる。

### ❌ 悪い例3: タイマーがクリアされない

```javascript
// タイマーリークの危険性
function startPolling() {
  const intervalId = setInterval(() => {
    fetchData();
  }, 5000);

  // clearInterval を忘れている
  // コンポーネントが破棄されてもタイマーが動き続ける
}
```

**問題点**: コンポーネントが破棄されてもタイマーが動き続け、不要なネットワークリクエストとメモリ使用が継続。

### ✅ 良い例1: try-finally でファイルをクローズ

```javascript
// 確実にファイルをクローズ
function readConfig(filePath) {
  const fs = require('fs');
  let fd;

  try {
    fd = fs.openSync(filePath, 'r');
    const buffer = Buffer.alloc(1024);
    fs.readSync(fd, buffer, 0, 1024, 0);
    return buffer.toString();
  } finally {
    if (fd !== undefined) {
      fs.closeSync(fd); // 必ず実行される
    }
  }
}
```

**理由**: `finally`句でファイルを確実にクローズ。例外が発生してもリソースリークを防ぐ。

### ✅ 良い例2: クリーンアップ関数でイベントリスナー解除

```javascript
// Reactの例: useEffect でクリーンアップ
function MyComponent() {
  useEffect(() => {
    const handleClick = () => {
      console.log('Button clicked');
    };

    const button = document.querySelector('#myButton');
    button.addEventListener('click', handleClick);

    // クリーンアップ関数でリスナー解除
    return () => {
      button.removeEventListener('click', handleClick);
    };
  }, []);

  return <div id="myButton">Click me</div>;
}
```

**理由**: コンポーネントがアンマウントされるときにイベントリスナーを自動的に解除。

### ✅ 良い例3: タイマーをクリーンアップ

```javascript
// Reactの例: useEffect でタイマークリア
function MyComponent() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchData();
    }, 5000);

    // クリーンアップ関数でタイマークリア
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return <div>Polling...</div>;
}
```

**理由**: コンポーネントがアンマウントされるときにタイマーを自動的にクリア。

### ✅ 良い例4: データベース接続プールを使用

```javascript
// 接続プールで自動管理
const { Pool } = require('pg');
const pool = new Pool({ max: 10 });

async function queryDatabase(sql) {
  const client = await pool.connect();

  try {
    const result = await client.query(sql);
    return result.rows;
  } finally {
    client.release(); // プールに返却
  }
}
```

**理由**: 接続プールを使うことで、接続の取得と返却が管理され、リソースリークを防ぐ。

### ✅ 良い例5: RAIIパターン（Rust/C++の例）

```rust
// Rustの例: ファイルは自動的にクローズされる
use std::fs::File;
use std::io::Read;

fn read_config(file_path: &str) -> std::io::Result<String> {
    let mut file = File::open(file_path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    Ok(contents)
    // file はスコープを抜けるときに自動的にクローズ（RAII）
}
```

**理由**: Rustはスコープを抜けるときに自動的にリソースを解放（Drop trait）。明示的なクローズ不要。

---

## 関連観点

- [C05] 例外安全性
- [PERF01] パフォーマンス
- [C01] バグ検出

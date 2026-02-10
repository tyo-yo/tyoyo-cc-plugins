# セキュリティ脆弱性（基本）

**ID**: S01
**カテゴリ**: セキュリティ（基本）
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点（明確）、80-90点（潜在的）

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Piebald-AI Security Review](https://github.com/Piebald-AI/claude-code-system-prompts)
- [anilcancakir/claude-code-plugins](https://github.com/anilcancakir/claude-code-plugins)

---

## 概要

この観点は、コード内の基本的なセキュリティリスクを特定します。OWASP Top 10などの一般的な脆弱性パターンを検出し、実際に悪用可能なセキュリティホールを防ぎます。

すべてのコード変更で適用され、特に入力検証、認証・認可、データ処理に関わるコードで重要です。

---

## チェック内容

- 入力検証の欠如
  - ユーザー入力の未検証
  - サニタイゼーションの欠如
  - 型チェックの不足
- SQLインジェクション脆弱性
  - 生のSQL文字列結合
  - パラメータ化クエリの未使用
  - ORM の安全でない使用
- XSS（クロスサイトスクリプティング）
  - ユーザー入力のエスケープ漏れ
  - innerHTML への直接代入
  - 安全でないテンプレート使用
- CSRF（クロスサイトリクエストフォージェリ）
  - CSRFトークンの欠如
  - SameSite属性の未設定
- コマンドインジェクション
  - シェルコマンドへのユーザー入力埋め込み
  - `eval`、`exec`の安全でない使用
- パストラバーサル
  - ファイルパスの未検証
  - ディレクトリトラバーサル攻撃
- 認証・認可の不備
  - 認証チェックの欠如
  - 権限チェックの不足
  - セッション管理の不備
- 機密データの不適切な処理
  - ログへの機密情報出力
  - 平文でのパスワード保存
  - エラーメッセージでの情報漏洩
- 安全でない依存関係の使用
  - 既知の脆弱性を持つライブラリ
  - 古いバージョンの使用
- ハードコードされた認証情報
  - コード内のパスワード、APIキー
  - 秘密鍵の埋め込み

---

## 適用基準

### 使用する場合

- ✅ 常に適用（すべてのコード変更）
- ✅ 特にユーザー入力処理
- ✅ 認証・認可ロジック
- ✅ データベースアクセス
- ✅ ファイル操作
- ✅ 外部コマンド実行

### 使用しない場合

- ❌ 該当なし（必須観点）

---

## 具体例

### ❌ 悪い例：SQLインジェクション

```python
def get_user_by_username(username):
    # 問題: ユーザー入力を直接SQL文字列に埋め込んでいる
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return database.execute(query)

# 攻撃例: username = "admin' OR '1'='1"
# 実行されるSQL: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# 結果: すべてのユーザーが取得される
```

**問題点**: ユーザー入力を直接SQL文に埋め込んでおり、SQLインジェクション攻撃が可能です。

### ✅ 良い例

```python
def get_user_by_username(username):
    # パラメータ化クエリを使用
    query = "SELECT * FROM users WHERE username = ?"
    return database.execute(query, (username,))
```

**理由**: パラメータ化クエリを使用し、ユーザー入力はデータとして扱われるためSQLインジェクションが防止されます。

---

### ❌ 悪い例：XSS（クロスサイトスクリプティング）

```javascript
function displayUserComment(comment) {
  const commentDiv = document.getElementById('comments');
  // 問題: ユーザー入力をエスケープせずにHTMLに挿入
  commentDiv.innerHTML += `<div>${comment}</div>`;
}

// 攻撃例: comment = "<script>alert(document.cookie)</script>"
// 結果: JavaScriptが実行される
```

**問題点**: ユーザー入力をエスケープせずにinnerHTMLに代入しており、XSS攻撃が可能です。

### ✅ 良い例

```javascript
function displayUserComment(comment) {
  const commentDiv = document.getElementById('comments');
  const div = document.createElement('div');
  // textContent を使用してテキストとして挿入
  div.textContent = comment;
  commentDiv.appendChild(div);
}
```

**理由**: `textContent`を使用することで、HTMLタグはエスケープされテキストとして表示されます。

---

### ❌ 悪い例：コマンドインジェクション

```python
import subprocess

def compress_file(filename):
    # 問題: ユーザー入力を直接シェルコマンドに埋め込んでいる
    subprocess.run(f"tar -czf {filename}.tar.gz {filename}", shell=True)

# 攻撃例: filename = "test.txt; rm -rf /"
# 実行されるコマンド: tar -czf test.txt; rm -rf /.tar.gz test.txt; rm -rf /
# 結果: システムのファイルが削除される
```

**問題点**: `shell=True`とユーザー入力の組み合わせにより、任意のコマンドが実行可能です。

### ✅ 良い例

```python
import subprocess
import os

def compress_file(filename):
    # ファイル名のバリデーション
    if not is_safe_filename(filename):
        raise ValueError("Invalid filename")

    # シェルを使わず、引数をリストで渡す
    subprocess.run(['tar', '-czf', f'{filename}.tar.gz', filename], shell=False)

def is_safe_filename(filename):
    # ディレクトリトラバーサルを防ぐ
    if '..' in filename or filename.startswith('/'):
        return False
    # ファイル名として許可する文字のみを許可
    return filename.replace('/', '').replace('\\', '').isalnum() or '.' in filename
```

**理由**: `shell=False`を使用し、引数をリストで渡すことでコマンドインジェクションを防止します。また、ファイル名のバリデーションも実施しています。

---

### ❌ 悪い例：パストラバーサル

```javascript
const express = require('express');
const fs = require('fs');
const path = require('path');

app.get('/download', (req, res) => {
  const filename = req.query.file;
  // 問題: ユーザー入力を直接ファイルパスに使用
  const filePath = path.join(__dirname, 'uploads', filename);
  res.sendFile(filePath);
});

// 攻撃例: /download?file=../../etc/passwd
// 結果: システムファイルが読み取られる
```

**問題点**: ユーザー入力を検証せずファイルパスに使用しており、ディレクトリトラバーサル攻撃が可能です。

### ✅ 良い例

```javascript
const express = require('express');
const fs = require('fs');
const path = require('path');

app.get('/download', (req, res) => {
  const filename = req.query.file;

  // ファイル名のバリデーション
  if (!filename || filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    return res.status(400).send('Invalid filename');
  }

  const uploadsDir = path.join(__dirname, 'uploads');
  const filePath = path.join(uploadsDir, filename);

  // パスが uploads ディレクトリ内であることを確認
  if (!filePath.startsWith(uploadsDir)) {
    return res.status(400).send('Invalid file path');
  }

  // ファイルの存在確認
  if (!fs.existsSync(filePath)) {
    return res.status(404).send('File not found');
  }

  res.sendFile(filePath);
});
```

**理由**: ファイル名のバリデーションと、最終的なパスが許可されたディレクトリ内であることを確認しています。

---

### ❌ 悪い例：ハードコードされた認証情報

```python
# 問題: APIキーがコードに直接埋め込まれている
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "MySecretPassword123"

def connect_to_api():
    return requests.get("https://api.example.com/data",
                       headers={"Authorization": f"Bearer {API_KEY}"})
```

**問題点**: 機密情報がコードに含まれており、バージョン管理システムに記録されます。

### ✅ 良い例

```python
import os

# 環境変数から読み込む
API_KEY = os.environ.get('API_KEY')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

if not API_KEY or not DATABASE_PASSWORD:
    raise ValueError("Required environment variables not set")

def connect_to_api():
    return requests.get("https://api.example.com/data",
                       headers={"Authorization": f"Bearer {API_KEY}"})
```

**理由**: 機密情報を環境変数から読み込み、コードには含めません。

---

### ❌ 悪い例：機密情報のログ出力

```typescript
async function login(username: string, password: string) {
  // 問題: パスワードをログに記録している
  logger.info(`Login attempt for user: ${username}, password: ${password}`);

  const user = await authenticateUser(username, password);

  if (user) {
    // 問題: セッショントークンをログに記録
    logger.info(`Login successful. Session token: ${user.sessionToken}`);
  }

  return user;
}
```

**問題点**: パスワードやセッショントークンがログファイルに平文で記録されます。

### ✅ 良い例

```typescript
async function login(username: string, password: string) {
  // ユーザー名のみをログに記録
  logger.info(`Login attempt`, { username });

  const user = await authenticateUser(username, password);

  if (user) {
    // セッション情報は記録しない、またはハッシュ値のみ
    logger.info(`Login successful`, { username, userId: user.id });
  }

  return user;
}
```

**理由**: 機密情報をログに記録せず、必要最小限の情報のみを記録します。

---

## 関連観点

- [S02] 一般的な脆弱性パターン
- [S03] False Positiveフィルタリング
- [C03] エッジケースとバウンダリー条件
- [C04] サイレントフェイラー

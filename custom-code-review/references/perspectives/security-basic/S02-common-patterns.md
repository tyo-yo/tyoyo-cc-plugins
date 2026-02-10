# 一般的な脆弱性パターン

**ID**: S02
**カテゴリ**: セキュリティ（基本）
**優先度**: Tier 2（推奨）
**信頼度基準**: 80-100点

---

## 参照元

- [trailofbits/skills](https://github.com/trailofbits/skills)
- [Trail of Bits Vulnerability Patterns](https://github.com/trailofbits/skills/blob/main/differential-review/differential-review.md)

---

## 概要

一般的な脆弱性パターンのカタログを使用して、コード変更が既知の脆弱性パターンに該当しないかを体系的にチェックします。Trail of Bitsのセキュリティレビュー経験に基づく、実際のコードで頻出する脆弱性パターンを対象とします。

この観点は、特にセキュリティ関連コード、認証・認可ロジック、外部API呼び出しなどの高リスク領域で有効です。

---

## チェック内容

### 認証・認可
- デフォルト認証情報の使用
- 認証バイパス可能な条件分岐
- セッション管理の欠陥
- JWT署名検証の欠如
- 権限昇格の可能性
- アクセス制御修飾子の削除

### 暗号化
- 弱い暗号アルゴリズム（MD5、SHA1、DES）
- ハードコードされた暗号鍵
- 安全でない乱数生成（Math.random()）
- 証明書検証のバイパス
- 暗号化されていない機密データ送信

### インジェクション
- SQLインジェクション（パラメータ化されていないクエリ）
- コマンドインジェクション（未検証の外部入力）
- パストラバーサル（ファイルパス検証不足）
- XXE（XML外部エンティティ）
- テンプレートインジェクション
- NoSQLインジェクション

### データ露出
- ハードコードされた認証情報
- 機密情報のログ出力
- PII（個人情報）の不適切な処理
- APIレスポンスでの過剰な情報露出
- デバッグ情報の本番環境への露出

### リソース管理
- リソースリークの可能性
- DOS可能な処理（無制限ループ、再帰）
- 外部呼び出しの無制限実行

---

## 適用基準

### 使用する場合

- ✅ セキュリティ関連コード変更
- ✅ 認証・認可ロジックの追加・変更
- ✅ 外部API呼び出しの追加
- ✅ データベースクエリの変更
- ✅ ファイル操作、パス処理の変更
- ✅ 暗号化処理の実装

### 使用しない場合

- ❌ 単純なバグ修正（セキュリティ無関係）
- ❌ ドキュメント変更のみ
- ❌ テストコード変更のみ（本番コード変更なし）

---

## 具体例

### ❌ 悪い例: SQLインジェクション

```python
# 未検証の入力を直接SQLに埋め込み
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

**問題点**: ユーザー入力が直接SQL文に埋め込まれており、`username = "' OR '1'='1"` のような攻撃が可能。

### ✅ 良い例: パラメータ化クエリ

```python
# パラメータ化クエリで安全に実装
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return db.execute(query, (username,))
```

**理由**: パラメータ化クエリを使用することで、ユーザー入力が実行可能なコードとして解釈されることを防ぎます。

---

### ❌ 悪い例: 弱い暗号アルゴリズム

```javascript
// MD5は衝突攻撃に脆弱
const crypto = require('crypto');
function hashPassword(password) {
  return crypto.createHash('md5').update(password).digest('hex');
}
```

**問題点**: MD5は既に脆弱性が知られており、パスワードハッシュとして不適切。レインボーテーブル攻撃や衝突攻撃が可能。

### ✅ 良い例: 安全なハッシュアルゴリズム

```javascript
// bcryptやscryptを使用
const bcrypt = require('bcrypt');
async function hashPassword(password) {
  const saltRounds = 10;
  return await bcrypt.hash(password, saltRounds);
}
```

**理由**: bcryptは計算コストが高く、ソルト付きでハッシュ化するため、ブルートフォース攻撃に対して強固。

---

### ❌ 悪い例: コマンドインジェクション

```python
# ユーザー入力をシェルコマンドに直接使用
import subprocess
def process_file(filename):
    # shell=Trueは危険
    subprocess.run(f"convert {filename} output.pdf", shell=True)
```

**問題点**: `filename = "input.jpg; rm -rf /"` のようなコマンドインジェクションが可能。

### ✅ 良い例: 安全な実行

```python
# サブプロセスのリスト形式で安全に実行
import subprocess
def process_file(filename):
    subprocess.run(["convert", filename, "output.pdf"], check=True)
```

**理由**: リスト形式で引数を渡すことで、シェルを経由せず、コマンドインジェクションを防ぎます。

---

## 2026年トレンド

AI生成コードでは、基本的な脆弱性パターン（SQLインジェクション、XSS）は減少傾向にある一方、以下のパターンが増加:

- **認証ロジックの微妙な欠陥**: 条件分岐の順序ミスによるバイパス
- **デフォルト設定の不適切な使用**: ライブラリのデフォルト設定が安全でない場合
- **不完全なバリデーション**: 一部の入力パスでバリデーションが漏れる

---

## 関連観点

- [S01] セキュリティ脆弱性（基本）
- [S03] False Positiveフィルタリング
- [S06] 攻撃者モデリング
- [S07] セキュリティリグレッション

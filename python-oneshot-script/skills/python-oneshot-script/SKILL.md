---
name: python-oneshot-script
description: This skill should be used when creating standalone utility scripts with "uv run", writing one-off Python tools, using PEP 723 inline metadata, or when the user asks to "write a utility script", "create a standalone script", "make a one-off Python tool", "scripts/ にスクリプトを作成". NOT for project source code (src/, lib/, app/).
allowed-tools: Bash(uv:*), Write, Read
---

# Python 単発スクリプト作成ガイドライン

`uv run` と PEP 723 インラインメタデータを使った、仮想環境不要の Python スクリプト作成ガイド。

## このスキルの適用範囲

### ✅ 使うべき場面

- `scripts/` ディレクトリに置くユーティリティスクリプト
- 単発の自動化ツール、データ処理スクリプト
- プロジェクトとは独立して動作するスタンドアロンツール
- 一時的な調査・検証用スクリプト

### ❌ 使わない場面

- **プロジェクトのソースコード**（`src/`、`lib/`、`app/` 以下）
- pyproject.toml で管理されるパッケージのモジュール
- pytest で実行するテストコード（`tests/`）
- プロジェクトの依存関係に含まれるべきコード

プロジェクトのソースコードは通常の Python モジュールとして書き、依存関係は pyproject.toml で管理する。

---

## 概要

- **仮想環境不要**: `uv run script.py` で依存関係を自動解決
- **自己完結型**: スクリプト内に依存関係を宣言
- **高速起動**: キャッシュにより2回目以降は数ミリ秒で起動

---

## スクリプトの分類と対応

### 一時的なスクリプト（使い捨て）

標準ライブラリのみ、または結果確認後に削除するスクリプト。

**対応**: シンプルに書く。メタデータ不要。

```python
# 現在時刻を取得する一時スクリプト
from datetime import datetime
print(datetime.now())
```

実行: `uv run script.py` または `python script.py`

### 永続スクリプト（プロジェクトに残す・再利用）

外部パッケージを使用する、または繰り返し使用するスクリプト。

**対応**: PEP 723 インラインメタデータを必ず記述する。

---

## PEP 723 インラインメタデータの書き方

### 基本形式

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "rich",
# ]
# ///

import requests
from rich import print

# スクリプト本体
```

### 必須要素

| 要素 | 説明 |
|------|------|
| `# /// script` | メタデータブロック開始（必須） |
| `# ///` | メタデータブロック終了（必須） |
| `dependencies = [...]` | 依存パッケージリスト（空でも必須） |
| `requires-python` | Python バージョン要件（推奨） |

### shebang について

```python
#!/usr/bin/env -S uv run --script
```

- shebang を付けると `./script.py` で直接実行可能
- `chmod +x script.py` で実行権限を付与すること
- shebang なしでも `uv run script.py` で実行可能

---

## 実行方法

```bash
# 基本実行
uv run script.py

# shebang付きスクリプトの直接実行
chmod +x script.py
./script.py

# Python バージョン指定
uv run --python 3.12 script.py

# アドホックに依存関係を追加（メタデータ未記載のパッケージ）
uv run --with pandas script.py
```

---

## プロジェクト内での注意

pyproject.toml があるディレクトリでスクリプトを実行すると、プロジェクトの依存関係もインストールされる。

スクリプトを独立して実行したい場合:
```bash
uv run --no-project script.py
```

ただし、PEP 723 メタデータがあるスクリプトはプロジェクト依存関係が自動的に無視される。

---

## やってはいけないこと

### ❌ プロジェクトソースコードに PEP 723 メタデータを使う

```python
# ❌ BAD: src/ 以下のモジュールにインラインメタデータ
# src/myapp/utils.py
# /// script
# dependencies = ["requests"]
# ///

# ✅ GOOD: プロジェクトソースコードは通常のモジュールとして書く
# src/myapp/utils.py
import requests  # pyproject.toml で管理
```

プロジェクトの依存関係は pyproject.toml で一元管理する。

### ❌ 外部パッケージ使用時にメタデータを省略

```python
# ❌ BAD: メタデータなしで外部パッケージを使用
import requests  # 依存関係が不明

resp = requests.get("https://api.example.com")
```

### ❌ dependencies フィールドの省略

```python
# ❌ BAD: 依存関係がなくても dependencies は必須
# /// script
# requires-python = ">=3.11"
# ///
```

正しくは:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

### ❌ uvx でスクリプトを実行

```bash
# ❌ BAD: uvx は CLIツール（ruff, black等）用
uvx script.py

# ✅ GOOD: スクリプトには uv run を使う
uv run script.py
```

### ❌ グローバル環境にパッケージをインストール

```bash
# ❌ BAD: グローバル環境を汚染
pip install requests
python script.py

# ✅ GOOD: uv run で隔離環境を使用
uv run script.py
```

---

## ベストプラクティス

### 1. 永続スクリプトには必ずメタデータを記述

プロジェクトに残す、git にコミットする、他の人と共有するスクリプトには必ず PEP 723 メタデータを記述する。

### 2. shebang を付けて実行可能にする

繰り返し使うスクリプトには shebang を付けて直接実行可能にする。

```python
#!/usr/bin/env -S uv run --script
```

### 3. バージョン制約を適切に指定

```python
# /// script
# dependencies = [
#   "requests>=2.31,<3",  # メジャーバージョンを制約
#   "rich>=13.0",
# ]
# ///
```

### 4. 再現性が必要ならロックファイルを作成

```bash
uv lock --script script.py
# script.py.lock が生成される
```

### 5. 日付制約で更なる再現性を確保（オプション）

```python
# /// script
# dependencies = ["requests"]
# [tool.uv]
# exclude-newer = "2024-01-01T00:00:00Z"
# ///
```

---

## スクリプト雛形の自動生成

```bash
# 新規スクリプト作成
uv init --script example.py --python 3.12

# 依存関係を追加
uv add --script example.py requests rich
```

---

## 判断フローチャート

```
Python コードを書く
    ↓
プロジェクトソースコード？（src/, lib/, app/, tests/）
    ├─ Yes → このスキルは使わない
    │        → 通常のモジュールとして書く（pyproject.toml で依存管理）
    └─ No → スタンドアロンスクリプト
              ↓
          外部パッケージを使う？
              ├─ No → 標準ライブラリのみ
              │        └─ 一時的？ → メタデータ不要でOK
              │        └─ 永続的？ → メタデータを書く（空の dependencies でも）
              └─ Yes → 必ずメタデータを書く
                        └─ 繰り返し使う？ → shebang も付ける
                        └─ 再現性必要？ → ロックファイルも作成
```

---

## 例

### 例1: API からデータ取得

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "rich>=13.0",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://api.github.com/repos/astral-sh/uv")
pprint(resp.json())
```

### 例2: ファイル処理（標準ライブラリのみ）

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
from pathlib import Path

data = json.loads(Path("data.json").read_text())
print(f"Keys: {list(data.keys())}")
```

### 例3: CLIツール

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click>=8.0",
#   "rich>=13.0",
# ]
# ///

import click
from rich.console import Console

console = Console()

@click.command()
@click.argument("name")
def greet(name: str):
    """Greet someone."""
    console.print(f"Hello, [bold green]{name}[/]!")

if __name__ == "__main__":
    greet()
```

---

## 追加リソース

### 参考リンク

- [uv - Running scripts](https://docs.astral.sh/uv/guides/scripts/)
- [PEP 723 – Inline script metadata](https://peps.python.org/pep-0723/)

### 例ファイル

- `examples/api-fetch.py` - API取得の完全な例
- `examples/cli-tool.py` - CLIツールの完全な例

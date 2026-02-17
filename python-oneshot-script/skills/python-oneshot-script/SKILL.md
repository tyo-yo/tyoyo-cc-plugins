---
name: python-oneshot-script
description: This skill should be used when creating standalone utility scripts with "uv run", writing one-off Python tools, using PEP 723 inline metadata, or when the user asks to "write a utility script", "create a standalone script", "make a one-off Python tool", "scripts/ にスクリプトを作成", "ワンショットスクリプトを書いて", "uv run で実行できるスクリプト". NOT for project source code (src/, lib/, app/).
allowed-tools: Bash(command:uv *), Write, Read
---

# Python 単発スクリプト作成ガイドライン

`uv run` と PEP 723 インラインメタデータを使った、仮想環境不要の Python スクリプト作成ガイド。

## 適用範囲

### ✅ 使うべき場面

- `scripts/` ディレクトリに置くユーティリティスクリプト
- データ変換・API取得・ファイル操作などの単発自動化ツール
- 一時的な調査・検証用スクリプト

### ❌ 使わない場面

- プロジェクトのソースコード（`src/`、`lib/`、`app/` 以下）
- pyproject.toml で管理されるパッケージのモジュール
- pytest で実行するテストコード（`tests/`）

---

## PEP 723 インラインメタデータ

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "typer>=0.20",
#   "loguru>=0.7",
# ]
# ///
```

### uv コマンド

```bash
# 実行
uv run script.py

# 依存関係をメタデータに自動挿入
uv add --script script.py httpx loguru

# ロックファイル（再現性が必要な場合）
uv lock --script script.py

# shebang 付きなら直接実行も可
chmod +x script.py && ./script.py
```

---

## ライブラリ早見表

| ユースケース | ライブラリ | 備考 |
|---|---|---|
| CLI 引数 | `typer` | Annotated スタイルで書く |
| リッチ出力 | `rich` | テーブル、プログレスバー |
| ロギング | `loguru` | 10行超のスクリプトで使う |
| HTTP リクエスト | `httpx` | requests の後継 |
| シェルコマンド実行 | `plumbum` | WSL/Linux/macOS 対応 |
| ネスト JSON アクセス | `glom` | KeyError なし・安全なパス指定 |
| JSON フィルタ・変換 | `jq` | jq 記法でクエリ・変換 |
| SQL でデータ集計 | `duckdb` | CSV/JSON/Parquet をサーバー不要で |

バージョン指定なし（`"typer"` のみ）で uv が最新を取得する。再現性が必要な場合のみ `uv lock --script` でロックする。

各ライブラリの使い方は `references/libraries.md` を参照。

---

## 品質方針

- **ハッピーパス優先**: エラーハンドリングは省略が基本。エラー発生時はメッセージを見て修正する
- **try/except は別動作が必要な時のみ**: 単に処理を止めたいだけなら不要（例外は自然に伝播する）
- **型ヒント必須**: 関数の引数・戻り値には型ヒントを書く
- **コメント・docstring 不要**: コード自体が自明になるよう書く
- **ロギング**: 10行以内は `print`、それ以上は `loguru`

---

## ボイラープレート

### CLI ツール（Typer + loguru）

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "typer",
#   "loguru",
# ]
# ///

import sys
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger

app = typer.Typer()


@app.command()
def main(
    input_file: Annotated[Path, typer.Argument(help="入力ファイル")],
    output: Annotated[Path, typer.Option("-o")] = Path("output.json"),
    verbose: Annotated[bool, typer.Option("-v")] = False,
) -> None:
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")
    logger.info("処理開始: {}", input_file)
    # ... 処理 ...
    logger.success("完了: {}", output)


app()
```

### シンプルスクリプト（stdlib + print）

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import json
from pathlib import Path

data = json.loads(Path("data.json").read_text())
print(data["result"])
```

---

## スクリプト分類

| タイプ | 目安 | メタデータ | shebang |
|---|---|---|---|
| 使い捨て | ~10行・stdlib のみ | 不要でも可 | 不要 |
| 永続スクリプト | 繰り返し使う・外部パッケージ | **必須** | 推奨 |

---

## やってはいけないこと

```python
# ❌ src/ 以下のモジュールに PEP 723 メタデータを使う
# ❌ 外部パッケージ使用時にメタデータを省略
# ❌ uvx でスクリプトを実行（uvx は ruff/black 等の CLI ツール用）
# ❌ pip install でグローバル環境を汚染
# ❌ dependencies フィールドを省略（空でも必須）
```

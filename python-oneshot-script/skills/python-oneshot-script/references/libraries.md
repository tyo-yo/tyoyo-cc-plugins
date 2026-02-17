# ライブラリ使い方リファレンス

ワンショットスクリプトで使う主要ライブラリのパターン集。

---

## typer — CLI 引数

型ヒントだけで引数・ヘルプ・補完が自動生成される。**Annotated スタイル**で書く。

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    src: Annotated[str, typer.Argument(help="入力ファイル")],
    fmt: Annotated[str, typer.Option("-f", help="出力形式")] = "json",
    verbose: Annotated[bool, typer.Option("-v")] = False,
) -> None:
    ...

app()
```

単一コマンドなら `typer.run(main)` でも可。サブコマンドが必要になったら `app = typer.Typer()` に移行する。

---

## rich — リッチ出力

テーブル・プログレスバー・カラー出力。`from rich import print` の1行で既存の print をリッチ版に置き換えられる。

```python
from rich import print
from rich.table import Table
from rich.progress import track

# カラー出力
print("[bold green]完了[/bold green]")

# テーブル
table = Table(title="結果")
table.add_column("ファイル", style="cyan")
table.add_column("件数", style="green")
table.add_row("data.csv", "1,234")
print(table)

# プログレスバー
for item in track(items, description="処理中..."):
    process(item)
```

---

## loguru — ロギング

設定ゼロでカラー付きログ。10行超のスクリプトで使う。

```python
import sys
from loguru import logger

# --verbose 対応
logger.remove()
logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")

logger.info("処理開始: {}", path)
logger.success("完了")
logger.warning("スキップ: {}", file)
logger.error("失敗: {}", e)

# ファイル出力が必要な場合
logger.add("app.log", rotation="10 MB")
```

---

## httpx — HTTP リクエスト

requests の後継。同期・非同期を同じライブラリで書ける。

```python
import httpx

# 同期（ワンショットでは基本こちら）
resp = httpx.get("https://api.example.com/data")
data = resp.json()

# ヘッダー・タイムアウト
resp = httpx.get(
    "https://api.example.com/data",
    headers={"Authorization": f"Bearer {token}"},
    timeout=30.0,
)

# POST
resp = httpx.post("https://api.example.com/items", json={"name": "foo"})

# 非同期（複数リクエストを並列処理したい場合）
import asyncio

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

---

## plumbum — シェルコマンド実行

WSL/Linux/macOS 対応。Windows ネイティブは非対応。
詳細は DeepWiki（`tomerfiliba/plumbum`）を参照。

```python
from plumbum.cmd import git, grep, wc
from plumbum import local, ProcessExecutionError

# 基本実行
output = git("log", "--oneline", "-5")

# 引数バインド → パイプ
result = (grep["-r", "TODO", "."] | wc["-l"])()

# retcode + stdout + stderr を取得
retcode, stdout, stderr = git.run("status")

# 特定の終了コードを成功とみなす（grep が 0件で exit 1 になる場合など）
retcode, out, _ = grep["pattern", "file.txt"].run(retcode=(0, 1))

# エラーハンドリング（別動作が必要な場合のみ）
try:
    git("push")
except ProcessExecutionError as e:
    print(e.retcode, e.stderr)

# cwd を一時変更
with local.cwd("/tmp"):
    ls = local["ls"]
    print(ls())
```

---

## glom — ネスト JSON アクセス

KeyError を出さずにネストを安全にたどる。Pure Python。

```python
from glom import glom, Coalesce

data = {"users": [{"name": "Alice", "address": {"city": "Tokyo"}}]}

# ドット記法でパスをたどる
glom(data, "users.0.address.city")              # "Tokyo"

# キーがなくても default で安全に
glom(data, "users.0.address.zip", default="")   # ""

# リスト全要素から特定フィールドを抽出
glom(data, ("users", ["name"]))                  # ["Alice"]

# 複数候補のどれかを試す
glom(data, Coalesce("user.nickname", "user.name", default="unknown"))
```

---

## jq — JSON フィルタ・変換

jq 記法で複雑なフィルタ・変換。Python パッケージのみで動作（CLI の jq は不要）。

```python
import jq

data = {"users": [{"name": "Alice", "active": True}, {"name": "Bob", "active": False}]}

# 最初の1件
jq.first(".users[0].name", data)                         # "Alice"

# フィルタして抽出
jq.all(".users[] | select(.active) | .name", data)       # ["Alice"]

# 変換
jq.first("[.users[] | {n: .name}]", data)                # [{"n": "Alice"}, {"n": "Bob"}]

# 文字列から直接パース
jq.first(".foo", '{"foo": 42}')                          # 42
```

---

## duckdb — SQL でデータ集計

サーバー不要・CSV/JSON/Parquet を直接 SQL でクエリ。ワンショット向き。

```python
import duckdb

# CSV を直接クエリ
result = duckdb.sql("SELECT category, AVG(price) FROM read_csv_auto('sales.csv') GROUP BY 1")
print(result)

# JSON を集計
result = duckdb.sql("SELECT COUNT(*) FROM read_json_auto('data.json') WHERE status = 'active'")
print(result.fetchone())

# pandas / polars に変換
df = duckdb.sql("SELECT * FROM read_csv_auto('data.csv') LIMIT 100").df()   # pandas
pl_df = duckdb.sql("SELECT * FROM 'data.parquet'").pl()                      # polars

# 複数ファイル結合
duckdb.sql("SELECT * FROM read_csv_auto('data/*.csv')")
```

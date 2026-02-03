#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "rich>=13.0",
# ]
# ///
"""
API からデータを取得して表示するサンプルスクリプト。

Usage:
    chmod +x api-fetch.py
    ./api-fetch.py
    # または
    uv run api-fetch.py
"""

import requests
from rich.console import Console
from rich.table import Table

console = Console()


def main():
    """GitHub API から uv リポジトリ情報を取得して表示."""
    url = "https://api.github.com/repos/astral-sh/uv"

    with console.status("Fetching data..."):
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

    data = resp.json()

    table = Table(title="astral-sh/uv Repository Info")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", data["full_name"])
    table.add_row("Stars", f"{data['stargazers_count']:,}")
    table.add_row("Forks", f"{data['forks_count']:,}")
    table.add_row("Language", data["language"])
    table.add_row("Description", data["description"][:60] + "...")

    console.print(table)


if __name__ == "__main__":
    main()

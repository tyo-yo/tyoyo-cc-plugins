#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click>=8.0",
#   "rich>=13.0",
# ]
# ///
"""
Click を使った CLI ツールのサンプルスクリプト。

Usage:
    chmod +x cli-tool.py
    ./cli-tool.py greet Alice
    ./cli-tool.py greet Alice --times 3
    # または
    uv run cli-tool.py greet Alice
"""

import click
from rich.console import Console

console = Console()


@click.group()
def cli():
    """Sample CLI tool demonstrating PEP 723 inline metadata."""
    pass


@cli.command()
@click.argument("name")
@click.option("--times", "-t", default=1, help="Number of times to greet")
def greet(name: str, times: int):
    """Greet someone by name."""
    for i in range(times):
        console.print(f"[bold green]Hello, {name}![/] ({i + 1}/{times})")


@cli.command()
@click.argument("numbers", nargs=-1, type=float)
def sum_numbers(numbers: tuple[float, ...]):
    """Calculate the sum of numbers."""
    if not numbers:
        console.print("[yellow]No numbers provided[/]")
        return
    result = sum(numbers)
    console.print(f"Sum of {numbers} = [bold cyan]{result}[/]")


if __name__ == "__main__":
    cli()

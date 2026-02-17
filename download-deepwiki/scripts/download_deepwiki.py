#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "typer",
#   "loguru",
#   "plumbum",
# ]
# ///

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from plumbum import local

DEFAULT_OUTPUT_DIR = Path(".kiro/deepwiki")
DEFAULT_MCP_CONFIG = Path(".mcp.json")
DEFAULT_SERVER = "private-deepwiki"

app = typer.Typer()


def mcpc_call(tool: str, args: dict, config: Path, server: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    with open(tmp_path, "w") as out_f:
        subprocess.run(
            ["mcpc", "--config", str(config), server, "tools-call", tool, json.dumps(args), "--json"],
            stdout=out_f,
            check=True,
        )
    data = json.loads(tmp_path.read_text(encoding="utf-8"))
    tmp_path.unlink(missing_ok=True)
    return data["content"][0]["text"]


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title).strip()
    return re.sub(r"[\s-]+", "_", slug)


def parse_structure(structure_text: str) -> dict[str, Path]:
    entries = []
    for line in structure_text.splitlines():
        if m := re.match(r"^\s*-\s+([\d.]+)\s+(.+)$", line):
            number = m.group(1)
            entries.append({"number": number, "title": m.group(2).strip(), "depth": len(number.split("."))})

    has_children: set[str] = set()
    for i in range(len(entries) - 1):
        if entries[i + 1]["depth"] > entries[i]["depth"]:
            has_children.add(entries[i]["number"])

    title_to_path: dict[str, Path] = {}
    dir_stack: list[tuple[int, str]] = []

    for entry in entries:
        number, title, depth = entry["number"], entry["title"], entry["depth"]
        slug = slugify(title)
        num_parts = number.split(".")
        dir_stack = [(d, n) for d, n in dir_stack if d < depth]
        path_prefix = Path(*[n for _, n in dir_stack]) if dir_stack else Path()

        if number in has_children:
            dir_name = f"{num_parts[0].zfill(2)}_{slug}" if depth == 1 else f"{number}_{slug}"
            title_to_path[title] = path_prefix / dir_name / "index.md"
            dir_stack.append((depth, dir_name))
        else:
            filename = f"{num_parts[0].zfill(2)}_{slug}.md" if depth == 1 else f"{number}_{slug}.md"
            title_to_path[title] = path_prefix / filename

    return title_to_path


def split_pages(content: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for page in re.split(r"(?=^# Page: )", content, flags=re.MULTILINE):
        if m := re.match(r"^# Page: (.+)$", page, re.MULTILINE):
            result[m.group(1).strip()] = page
    return result


@app.command()
def main(
    repo: Annotated[str, typer.Argument(help="対象リポジトリ（owner/repo）")],
    output_dir: Annotated[Path, typer.Option("--output-dir")] = DEFAULT_OUTPUT_DIR,
    mcp_config: Annotated[Path, typer.Option("--mcp-config")] = DEFAULT_MCP_CONFIG,
    server: Annotated[str, typer.Option("--server")] = DEFAULT_SERVER,
    no_clean: Annotated[bool, typer.Option("--no-clean")] = False,
) -> None:
    logger.remove()
    logger.add(sys.stderr, colorize=True)

    logger.info("repo: {}  output: {}", repo, output_dir.resolve())

    logger.info("[1/3] Fetching wiki structure...")
    title_to_path = parse_structure(mcpc_call("read_wiki_structure", {"repoName": repo}, mcp_config, server))
    logger.info("      {} pages found", len(title_to_path))

    logger.info("[2/3] Fetching wiki contents...")
    pages = split_pages(mcpc_call("read_wiki_contents", {"repoName": repo}, mcp_config, server))
    logger.info("      {} pages fetched", len(pages))

    logger.info("[3/3] Saving...")
    if not no_clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    unmatched = []
    for title, page_content in pages.items():
        rel_path = title_to_path.get(title) or Path(f"{slugify(title)}.md")
        if title not in title_to_path:
            unmatched.append(title)
        (output_dir / rel_path).parent.mkdir(parents=True, exist_ok=True)
        (output_dir / rel_path).write_text(page_content, encoding="utf-8")

    if unmatched:
        logger.warning("{} pages unmatched (saved to root): {}", len(unmatched), unmatched)

    logger.success("Done! {} pages → {}", len(pages), output_dir.resolve())


app()

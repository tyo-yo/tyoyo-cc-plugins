#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
DeepWiki Downloader

mcpc 経由で private-deepwiki MCP サーバーから Wiki コンテンツを取得し、
番号階層を保ったままローカルのマークダウンとして保存する。

Usage:
    uv run download_deepwiki.py --repo owner/repo
    uv run download_deepwiki.py --repo owner/repo --output-dir .kiro/deepwiki
    uv run download_deepwiki.py --repo owner/repo --no-clean

Requirements:
    - mcpc がインストール済み（npm install -g mcpc）
    - DEVIN_API_KEY 環境変数が設定済み
    - .mcp.json に private-deepwiki サーバーが設定済み
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def mcpc_call(tool: str, args: dict, mcp_config: Path, server: str) -> str:
    """mcpc 経由で MCP ツールを呼び出し、テキスト結果を返す。

    stdout が大きくなる場合があるため、一時ファイル経由で受け取る。
    """
    import tempfile

    cmd = [
        "mcpc", "--config", str(mcp_config),
        server, "tools-call", tool,
        json.dumps(args), "--json",
    ]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        with open(tmp_path, "w") as out_f:
            subprocess.run(cmd, stdout=out_f, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] mcpc {tool} failed:\n{e.stderr.decode()}", file=sys.stderr)
        tmp_path.unlink(missing_ok=True)
        sys.exit(1)
    data = json.loads(tmp_path.read_text(encoding="utf-8"))
    tmp_path.unlink(missing_ok=True)
    return data["content"][0]["text"]


def slugify(title: str) -> str:
    """タイトルをファイルシステムに安全なスラグに変換する。"""
    slug = re.sub(r"[^\w\s-]", "", title).strip()
    slug = re.sub(r"[\s-]+", "_", slug)
    return slug


def parse_structure(structure_text: str) -> dict[str, Path]:
    """ウィキ構造テキストを title -> 相対パス のマッピングに変換する。

    子を持つノードはディレクトリ（自身のコンテンツは index.md）になり、
    末端ノードは親ディレクトリ直下の .md ファイルとして保存される。
    """
    entries = []
    for line in structure_text.splitlines():
        m = re.match(r"^\s*-\s+([\d.]+)\s+(.+)$", line)
        if not m:
            continue
        number = m.group(1)
        title = m.group(2).strip()
        depth = len(number.split("."))
        entries.append({"number": number, "title": title, "depth": depth})

    # 子を持つノードを特定
    has_children: set[str] = set()
    for i in range(len(entries) - 1):
        if entries[i + 1]["depth"] > entries[i]["depth"]:
            has_children.add(entries[i]["number"])

    title_to_path: dict[str, Path] = {}
    dir_stack: list[tuple[int, str]] = []  # (depth, dir_name)

    for entry in entries:
        number = entry["number"]
        title = entry["title"]
        depth = entry["depth"]
        slug = slugify(title)
        num_parts = number.split(".")

        # 現在の深さより深いスタックエントリを除去
        dir_stack = [(d, n) for d, n in dir_stack if d < depth]

        # 祖先ディレクトリのパスを構築
        path_prefix = Path(*[n for _, n in dir_stack]) if dir_stack else Path()

        if number in has_children:
            # 子を持つノード → ディレクトリ化、コンテンツは index.md
            dir_name = f"{num_parts[0].zfill(2)}_{slug}" if depth == 1 else f"{number}_{slug}"
            rel_path = path_prefix / dir_name / "index.md"
            dir_stack.append((depth, dir_name))
        else:
            # 末端ノード → .md ファイル
            filename = f"{num_parts[0].zfill(2)}_{slug}.md" if depth == 1 else f"{number}_{slug}.md"
            rel_path = path_prefix / filename

        title_to_path[title] = rel_path

    return title_to_path


def split_pages(content: str) -> dict[str, str]:
    """ウィキコンテンツを {title: page_content} に分割する。"""
    pages = re.split(r"(?=^# Page: )", content, flags=re.MULTILINE)
    result: dict[str, str] = {}
    for page in pages:
        if not page.strip():
            continue
        m = re.match(r"^# Page: (.+)$", page, re.MULTILINE)
        if m:
            result[m.group(1).strip()] = page
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download DeepWiki as hierarchical markdown files"
    )
    parser.add_argument("--repo", required=True,
                        help="対象リポジトリ（owner/repo 形式）")
    parser.add_argument("--output-dir", type=Path, default=Path(".kiro/deepwiki"),
                        help="保存先ディレクトリ（デフォルト: .kiro/deepwiki）")
    parser.add_argument("--mcp-config", type=Path, default=Path(".mcp.json"),
                        help="mcpc 設定ファイルのパス（デフォルト: .mcp.json）")
    parser.add_argument("--server", default="private-deepwiki",
                        help="MCP サーバー名（デフォルト: private-deepwiki）")
    parser.add_argument("--no-clean", action="store_true",
                        help="既存ファイルを削除せず差分更新する")
    args = parser.parse_args()

    output_dir: Path = args.output_dir
    mcp_config: Path = args.mcp_config
    repo: str = args.repo
    server: str = args.server

    if not mcp_config.exists():
        print(f"[ERROR] .mcp.json not found: {mcp_config}", file=sys.stderr)
        print("       SETUP.md を参照してセットアップしてください", file=sys.stderr)
        sys.exit(1)

    print(f"Repo   : {repo}")
    print(f"Output : {output_dir.resolve()}")

    # Step 1: 構造取得
    print("\n[1/3] Fetching wiki structure...")
    structure_text = mcpc_call("read_wiki_structure", {"repoName": repo}, mcp_config, server)
    title_to_path = parse_structure(structure_text)
    print(f"       {len(title_to_path)} pages found")

    # Step 2: コンテンツ取得
    print("[2/3] Fetching wiki contents...")
    content = mcpc_call("read_wiki_contents", {"repoName": repo}, mcp_config, server)
    pages = split_pages(content)
    print(f"       {len(pages)} pages fetched")

    # Step 3: 保存
    print("[3/3] Saving pages...")
    if not args.no_clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = 0
    unmatched = []
    for title, page_content in pages.items():
        rel_path = title_to_path.get(title) or Path(f"{slugify(title)}.md")
        if title not in title_to_path:
            unmatched.append(title)

        full_path = output_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(page_content, encoding="utf-8")
        print(f"       {rel_path}")
        saved += 1

    if unmatched:
        print(f"\nWarning: {len(unmatched)} pages not matched to structure (saved to root):")
        for t in unmatched:
            print(f"  - {t}")

    print(f"\nDone! {saved} pages saved to {output_dir.resolve()}")


if __name__ == "__main__":
    main()

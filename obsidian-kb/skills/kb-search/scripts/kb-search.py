#!/usr/bin/env python3
"""KB semantic retrieval — thin wrapper over search.py.

Usage:
  kb-search.py query "descriptive search text" [--limit N]
  kb-search.py similar <slug> [--limit N]

Reads vault path from $OBSIDIAN_KB_VAULT env var.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SEARCH_SCRIPT = Path(__file__).parent / "search.py"


def get_vault():
    vault = os.environ.get("OBSIDIAN_KB_VAULT")
    if not vault:
        print("OBSIDIAN_KB_VAULT env var unset.", file=sys.stderr)
        sys.exit(1)
    return vault


def ir_query(text, vault, limit, via_stdin=False):
    """Run search.py and return raw JSON output."""
    cmd = ["uv", "run", str(SEARCH_SCRIPT), vault, "--json", "-k", str(limit)]
    if not via_stdin:
        cmd.insert(4, text)  # insert query after vault arg
    result = subprocess.run(
        cmd,
        input=text if via_stdin else None,
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def cmd_query(text, vault, limit):
    """Semantic search by query text."""
    raw = ir_query(text, vault, limit)
    entries = json.loads(raw)
    out = [
        {"slug": e["doc_id"].removesuffix(".md"), "score": e["score"]}
        for e in entries
    ]
    print(json.dumps(out, indent=2))


def cmd_similar(slug, vault, limit):
    """Find notes similar to a given slug."""
    note_path = os.path.join(vault, f"{slug}.md")
    if not os.path.exists(note_path):
        print(f"Note not found: {note_path}", file=sys.stderr)
        sys.exit(1)

    with open(note_path) as f:
        text = f.read()

    raw = ir_query(text, vault, limit + 1, via_stdin=True)
    entries = json.loads(raw)
    out = [
        {"slug": e["doc_id"].removesuffix(".md"), "score": e["score"]}
        for e in entries
        if e["doc_id"].removesuffix(".md") != slug
    ][:limit]
    print(json.dumps(out, indent=2))


def main():
    parser = argparse.ArgumentParser(description="KB semantic retrieval")
    sub = parser.add_subparsers(dest="mode", required=True)

    q = sub.add_parser("query", help="Semantic search by text")
    q.add_argument("text", help="Search query")
    q.add_argument("--limit", type=int, default=5)

    s = sub.add_parser("similar", help="Find notes similar to a slug")
    s.add_argument("slug", help="Note slug (without .md)")
    s.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    vault = get_vault()

    if args.mode == "query":
        cmd_query(args.text, vault, args.limit)
    elif args.mode == "similar":
        cmd_similar(args.slug, vault, args.limit)


if __name__ == "__main__":
    main()

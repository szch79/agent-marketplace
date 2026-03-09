#!/usr/bin/env python3
"""Resolve a citekey to a local file path.

Usage: resolve-citekey.py <citekey>

Supports:
  path%/abs/path    → prints the path as-is
  zotero%key        → queries Better BibTeX JSON-RPC for the PDF attachment path
  repo%name         → prints $OBSIDIAN_KB_VAULT/ZOB_assets/repos/<name>/
  url%https://...    → prints the URL as-is

Prints the resolved path on stdout. Exits 1 if not found.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path


BETTER_BIBTEX_URL = "http://localhost:23119/better-bibtex/json-rpc"


def resolve_path(key):
    return key


def resolve_zotero(citekey):
    """Query Better BibTeX for the PDF attachment path."""
    # First get the item to find its library ID
    item = bbt_request("item.search", [citekey])
    if not item:
        print(f"No Zotero item found for citekey: {citekey}", file=sys.stderr)
        sys.exit(1)

    # Find exact match
    match = next((i for i in item if i.get('citekey') == citekey), None)
    if not match:
        print(f"No exact match for citekey: {citekey}", file=sys.stderr)
        sys.exit(1)

    library_id = match.get('libraryID', 1)

    # Get attachments
    attachments = bbt_request("item.attachments", [citekey, library_id])
    if not attachments:
        print(f"No attachments for citekey: {citekey}", file=sys.stderr)
        sys.exit(1)

    # Find PDF attachment
    for att in attachments:
        path = att.get('path', '')
        if path.lower().endswith('.pdf'):
            return path

    # Fall back to first attachment with a path
    for att in attachments:
        path = att.get('path', '')
        if path:
            return path

    print(f"No file attachment found for citekey: {citekey}", file=sys.stderr)
    sys.exit(1)


def resolve_repo(name):
    vault = os.environ.get('OBSIDIAN_KB_VAULT')
    if not vault:
        print('OBSIDIAN_KB_VAULT env var unset.', file=sys.stderr)
        sys.exit(1)
    return str(Path(vault) / 'ZOB_assets' / 'repos' / name)


def bbt_request(method, params):
    """Make a JSON-RPC request to Better BibTeX."""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }).encode()

    req = urllib.request.Request(
        BETTER_BIBTEX_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            if "error" in data:
                print(f"BBT error: {data['error']}", file=sys.stderr)
                sys.exit(1)
            return data.get("result")
    except urllib.error.URLError:
        print("Cannot connect to Zotero/Better BibTeX. Is Zotero running?", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: resolve-citekey.py <citekey>", file=sys.stderr)
        sys.exit(1)

    citekey = sys.argv[1]

    if citekey.startswith('path%'):
        path = resolve_path(citekey[5:])
    elif citekey.startswith('zotero%'):
        path = resolve_zotero(citekey[7:])
    elif citekey.startswith('repo%'):
        path = resolve_repo(citekey[5:])
    elif citekey.startswith('url%'):
        path = citekey[4:]
    else:
        print(f"Unknown citekey prefix: {citekey}", file=sys.stderr)
        print("Must start with path%, zotero%, repo%, or url%", file=sys.stderr)
        sys.exit(1)

    print(path)


if __name__ == '__main__':
    main()

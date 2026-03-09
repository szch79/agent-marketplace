#!/usr/bin/env python3
"""Lean library search — unified interface to 6 search APIs."""

import json
import sys
import urllib.parse
import urllib.request

APIS = {
    "leansearch": {
        "url": "https://leansearch.net/search",
        "method": "POST",
    },
    "loogle": {
        "url": "https://loogle.lean-lang.org/json",
        "method": "GET",
    },
    "leanfinder": {
        "url": "https://bxrituxuhpc70w8w.us-east-1.aws.endpoints.huggingface.cloud",
        "method": "POST",
    },
    "state_search": {
        "url": "https://premise-search.com/api/search",
        "method": "GET",
    },
    "hammer_premise": {
        "url": "http://leanpremise.net/retrieve",
        "method": "POST",
    },
}


def fetch(url, data=None, headers_extra=None):
    headers = {"User-Agent": "mathlib-search/1.0"}
    if data:
        headers["Content-Type"] = "application/json"
    if headers_extra:
        headers.update(headers_extra)
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())



def leansearch(query):
    raw = fetch(APIS["leansearch"]["url"], {"query": [query], "num_results": "5"})
    for item in (raw[0] or [])[:5]:
        r = item.get("result", {})
        name = ".".join(r.get("name", []))
        typ = r.get("type", "")
        if name:
            print(f"{name} : {typ}")


def semantic(query):
    """Natural language search via leansearch."""
    leansearch(query)


def loogle(query):
    encoded = urllib.parse.quote(query)
    raw = fetch(f"{APIS['loogle']['url']}?q={encoded}")
    if raw.get("error"):
        print(f"error: {raw['error']}", file=sys.stderr)
        return
    for hit in (raw.get("hits") or [])[:8]:
        name = hit.get("name", "")
        typ = hit.get("type", "").strip()
        mod = hit.get("module", "")
        print(f"{name} : {typ}  [{mod}]")


def leanfinder(query):
    raw = fetch(APIS["leanfinder"]["url"], {"inputs": query, "top_k": 5})
    for r in raw.get("results", []):
        url = r.get("url", "")
        # extract name from url like "...pattern=Nat.add_comm#doc"
        name = ""
        if "pattern=" in url:
            name = url.split("pattern=")[-1].split("#")[0]
        formal = r.get("formal_statement", "")
        if name and formal:
            print(f"{name} : {formal}")
        elif name:
            informal = r.get("informal_statement", "")
            print(f"{name} — {informal}")
        elif formal:
            print(formal)


def state_search(query):
    encoded = urllib.parse.quote(query)
    raw = fetch(f"{APIS['state_search']['url']}?query={encoded}&results=5&rev=v4.22.0")
    for item in raw or []:
        name = item.get("name", "") if isinstance(item, dict) else str(item)
        if name:
            print(name)


def hammer_premise(query):
    raw = fetch(APIS["hammer_premise"]["url"], {"state": query, "new_premises": [], "k": 16})
    for item in raw or []:
        name = item.get("name", "") if isinstance(item, dict) else str(item)
        if name:
            print(name)


COMMANDS = {
    "semantic": semantic,
    "leansearch": leansearch,
    "loogle": loogle,
    "leanfinder": leanfinder,
    "state_search": state_search,
    "hammer_premise": hammer_premise,
}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <api> \"<query>\"", file=sys.stderr)
        print(f"APIs: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)

    api = sys.argv[1]
    query = " ".join(sys.argv[2:])

    if api not in COMMANDS:
        print(f"Unknown API: {api}. Choose from: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)

    try:
        COMMANDS[api](query)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

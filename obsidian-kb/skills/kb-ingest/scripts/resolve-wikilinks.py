#!/usr/bin/env python3
"""Batch-resolve wikilinks against the vault.

Usage:
  resolve-wikilinks.py slug1 slug2 ...          # read these articles
  resolve-wikilinks.py --follow slug1 slug2 ...  # read + follow outgoing links

Reads vault path from $OBSIDIAN_KB_VAULT env var.

Prints content only for slugs that resolve. Unresolved slugs are silently skipped.
Handles [[slug|alias]] format (strips alias part).

With --follow, extracts all [[wikilinks]] from resolved articles and appends
their content too (one level deep, no recursion). Duplicates are skipped.
"""

import os
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


def clean_slug(raw):
    """Strip [[]], alias, and whitespace."""
    s = raw.strip('[] ')
    if '|' in s:
        s = s.split('|')[0]
    return s


def read_note(vault, slug):
    """Read a note's content, return (slug, content) or None."""
    path = vault / f'{slug}.md'
    if path.is_file():
        return slug, path.read_text()
    return None


def extract_wikilinks(content):
    """Extract all wikilink slugs from markdown content."""
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(content)]


def print_note(slug, content):
    print(f'=== {slug} ===')
    print(content)
    print()


def main():
    vault_path = os.environ.get('OBSIDIAN_KB_VAULT')
    if not vault_path:
        print('OBSIDIAN_KB_VAULT env var unset.', file=sys.stderr)
        sys.exit(1)

    vault = Path(vault_path)
    if not vault.is_dir():
        print(f'Vault not found: {vault_path}', file=sys.stderr)
        sys.exit(1)

    args = sys.argv[1:]
    follow = False
    if args and args[0] == '--follow':
        follow = True
        args = args[1:]

    if not args:
        print('Usage: resolve-wikilinks.py [--follow] slug1 slug2 ...', file=sys.stderr)
        sys.exit(1)

    seen = set()
    linked_slugs = []

    # First pass: resolve requested slugs
    for raw in args:
        slug = clean_slug(raw)
        if slug in seen:
            continue
        seen.add(slug)
        result = read_note(vault, slug)
        if result:
            print_note(*result)
            if follow:
                for link in extract_wikilinks(result[1]):
                    if link not in seen:
                        linked_slugs.append(link)

    # Second pass (--follow only): resolve outgoing links, one level deep
    if follow:
        for slug in linked_slugs:
            if slug in seen:
                continue
            seen.add(slug)
            result = read_note(vault, slug)
            if result:
                print_note(*result)


if __name__ == '__main__':
    main()

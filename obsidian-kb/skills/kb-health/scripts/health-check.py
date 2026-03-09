#!/usr/bin/env python3
"""Run health checks on the KB vault and output a JSON report.

Usage: health-check.py
Reads vault path from $OBSIDIAN_KB_VAULT env var.

Checks:
- Orphan notes (not linked from any other note)
- Oversized articles (>250 lines)
"""

import json
import os
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
MAX_LINES = 250


def get_vault():
    vault_path = os.environ.get('OBSIDIAN_KB_VAULT')
    if not vault_path:
        print('OBSIDIAN_KB_VAULT env var unset.', file=sys.stderr)
        sys.exit(1)
    path = Path(vault_path)
    if not path.is_dir():
        print(f'Vault not found: {vault_path}', file=sys.stderr)
        sys.exit(1)
    return path


def main():
    vault_path = get_vault()

    # Collect all notes and their content
    notes = {}
    for md_file in sorted(vault_path.glob('*.md')):
        slug = md_file.stem
        text = md_file.read_text()
        notes[slug] = text

    # Find all outgoing wikilinks per note
    all_linked = set()
    for text in notes.values():
        for m in WIKILINK_RE.finditer(text):
            all_linked.add(m.group(1).strip())

    # Orphans: notes that exist but aren't linked from any other note
    orphans = [slug for slug in notes if slug not in all_linked]

    # Oversized: notes exceeding MAX_LINES
    oversized = []
    for slug, text in notes.items():
        line_count = len(text.splitlines())
        if line_count > MAX_LINES:
            oversized.append({'file': f'{slug}.md', 'lines': line_count})

    report = {
        'orphans': orphans,
        'oversized': oversized,
    }

    json.dump(report, sys.stdout, indent=2)
    print()


if __name__ == '__main__':
    main()

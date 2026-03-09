#!/usr/bin/env python3
"""Create a KB note, written directly to the vault.

Usage:
  create-note.py <slug> --body-file /tmp/body.md [--citekey <key>]

Reads vault path from $OBSIDIAN_KB_VAULT env var.
If --citekey is provided, wraps body with minimal frontmatter.
"""

import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Create a KB note')
    parser.add_argument('slug')
    parser.add_argument('--body-file', required=True)
    parser.add_argument('--citekey', default='')
    args = parser.parse_args()

    # Validate citekey format
    if args.citekey:
        valid_prefixes = ('path%', 'zotero%', 'repo%', 'url%')
        if not args.citekey.startswith(valid_prefixes):
            prefixes = ', '.join(valid_prefixes)
            print(
                f'Invalid citekey "{args.citekey}". '
                f'Must start with: {prefixes}',
                file=sys.stderr,
            )
            sys.exit(1)

    vault_path = os.environ.get('OBSIDIAN_KB_VAULT')
    if not vault_path:
        print('OBSIDIAN_KB_VAULT env var unset.', file=sys.stderr)
        sys.exit(1)

    body = Path(args.body_file).read_text()

    if args.citekey:
        content = f'---\ncitekey: {args.citekey}\n---\n\n{body}'
    else:
        content = body

    dest = Path(vault_path) / f'{args.slug}.md'
    dest.write_text(content)

    print(args.slug)


if __name__ == '__main__':
    main()

#!/usr/bin/env bash
# Clone a repo into the vault's ZOB_assets/repos/ and register it in REPOS.md.
# Usage: clone-repo.sh <clone-url>
# Reads vault path from $OBSIDIAN_KB_VAULT env var.
# Prints the repo name on success.

set -euo pipefail

url="$1"
vault="${OBSIDIAN_KB_VAULT:?Set OBSIDIAN_KB_VAULT env var}"

# Derive repo name from URL (strip trailing .git, take last path component)
name="$(basename "$url" .git)"

repos_dir="$vault/ZOB_assets/repos"
dest="$repos_dir/$name"
manifest="$repos_dir/REPOS.md"

if [[ -d "$dest" ]]; then
  echo "$name" # already cloned
  exit 0
fi

mkdir -p "$repos_dir"
git clone --depth 1 "$url" "$dest" >&2

# Create or append to REPOS.md (skip if already listed)
if [[ ! -f "$manifest" ]]; then
  cat > "$manifest" <<EOF
# Repos

| Name | URL |
|------|-----|
| $name | $url |
EOF
elif ! grep -q "| $name |" "$manifest"; then
  echo "| $name | $url |" >> "$manifest"
fi

echo "$name"

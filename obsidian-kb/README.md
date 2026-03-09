# obsidian-kb

A plugin that turns an Obsidian vault into a progressively-refined knowledge base. An agent can ingest sources (PDFs, Zotero items, code repos), extract knowledge from conversations, and deepen articles by revisiting raw sources.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `kb-ingest` | "ingest this paper", "add this repo to KB" | Ingests a source into a curated KB article (see supported types below) |
| `kb-distill` | "distill the KB", "save what we learned" | Distills reusable knowledge from the current conversation |
| `kb-refine` | (model-invoked) | Deepens an existing KB article with more detail |
| `kb-search` | (model-invoked) | Teaches the agent how to search the KB via semantic similarity |
| `kb-health` | "check KB health", "run KB diagnostics" | Checks vault consistency (oversized notes, weakly-linked notes) |

## Ingestion types

| Type | Example | How it's resolved |
|------|---------|-------------------|
| **Zotero** | `darwiche02:knowledge_compilation_map` | Citekey → local PDF via Better BibTeX |
| **PDF / file** | `~/Documents/thesis.pdf` | Read directly |
| **URL** | `https://react.dev/learn/hooks` | Available web fetch tool, follows same-domain subpages |
| **Git repo** | `https://github.com/foo/bar` | Cloned locally |

Append a focus hint to scope extraction: `/kb-ingest darwiche02:kc_map focus on DNNF and d-DNNF`

## Prerequisites

### 1. Obsidian vault

Create or designate an Obsidian vault for the KB. The plugin writes markdown files directly to this vault.

### 2. Environment variable

Set `OBSIDIAN_KB_VAULT` to the absolute path of your vault. Either in your
shell profile, Claude Code's settings (user level `~/.claude/settings.local.json` or project level `.claude/settings.local.json`), or the equivalent Codex environment configuration:

```json
{
  "env": {
    "OBSIDIAN_KB_VAULT": "/Users/you/Documents/MyVault"
  }
}
```

### 3. Project-level permissions

The plugin invokes scripts via `python3`. Add this rule to your **project's** `.claude/settings.json` to avoid permission prompts:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 *obsidian-kb/*)"
    ]
  }
}
```

### 4. Exclude asset files

Exclude `ZOB_assets/` from Obsidian's file index so cloned repos don't pollute search:

**Settings → Files and links → Advanced → Excluded files** → add `ZOB_assets/`

### 5. Zotero (optional)

For Zotero ingestion, you need:
- Zotero running locally with the Better BibTeX plugin (for citekeys)
- The `resolve-citekey.py` script queries Better BibTeX's JSON-RPC API directly

## How it works

Articles are plain markdown files linked via `[[wikilinks]]`. Notes ingested from external sources have a `citekey` in frontmatter (e.g., `citekey: path%/path/to/file.pdf`) so the agent can resolve back to the raw source when needed. Structure emerges organically from wikilinks — discovery is through semantic search.

The lookup policy in `CLAUDE.md` teaches the agent to check the KB before reaching for raw sources or web search, and to flag gaps when knowledge is missing.

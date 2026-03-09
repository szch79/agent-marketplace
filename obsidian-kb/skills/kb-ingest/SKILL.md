---
name: kb-ingest
description: "Ingest a source (PDF, Zotero item, code repository, or URL) into the Obsidian knowledge base — creates a curated article with key concepts and references. Use whenever the user wants to add something to the KB, says 'ingest this', 'add this paper/repo/PDF/article to KB', 'index this', or invokes /kb-ingest or $kb-ingest. Also triggers for 'create a KB article from this', 'add this to my knowledge base', or any mention of importing academic papers, codebases, web articles, documentation, or documents into the vault."
disable-model-invocation: true
---

# Ingestion

Ingest a source into the KB: resolve the source, read it, extract knowledge,
create a note, and evolve the corpus.

## Step 1: Determine source type and key

Parse $ARGUMENTS to determine source type, key, and optional focus hints.

The first token determines the source. Auto-detect the type from its shape —
do NOT split on `:` since citekeys contain colons:

- Starts with `/` or `~` or `.` → **path** (file path)
- `git@...` or `http` URL ending in `.git` or bare `github.com/owner/repo` shape → **repo** (clone URL)
- `http` URL (anything else) → **url** (web article or documentation)
- Otherwise → **zotero** (the entire first token is the Better BibTeX citekey, verbatim)

Any text after the source key is a **focus hint** — free-form instructions
that scope what to extract (e.g., "focus on chapters 3-5", "just the
algorithms", "skip proofs"). Pass the hint through to Step 4.

Invocation examples. Claude Code users can invoke `/kb-ingest`; Codex users
can invoke `$kb-ingest` with the same arguments:
- `/kb-ingest darwiche02:knowledge_compilation_map` → zotero, citekey = `darwiche02:knowledge_compilation_map`, no focus
- `/kb-ingest darwiche02:knowledge_compilation_map focus on DNNF and d-DNNF` → zotero, focus = "focus on DNNF and d-DNNF"
- `/kb-ingest ~/Documents/thesis.pdf chapters 1-3 only` → path, focus = "chapters 1-3 only"
- `/kb-ingest https://github.com/foo/bar` → repo, no focus
- `/kb-ingest https://react.dev/learn/hooks focus on custom hooks` → url, focus = "focus on custom hooks"
- `/kb-ingest https://arxiv.org/abs/2301.00001` → url, no focus
- `$kb-ingest https://react.dev/learn/hooks focus on custom hooks` → url, focus = "focus on custom hooks"

If $ARGUMENTS is empty, ask the user for type and key.

## Step 2: Resolve the source

**For zotero type** — resolve citekey to local PDF path:
```bash
pdf_path=$(python3 <skill-dir>/scripts/resolve-citekey.py "zotero%<citekey>")
```

**For repo type** — clone the repository:
```bash
repo_name=$(<skill-dir>/scripts/clone-repo.sh "<clone-url>")
```

**For path type** — use the file path directly.

**For url type** — no resolution needed. Use the available web fetch tool to read the URL directly.

## Step 3: Read the reference guide

Read the type-specific reference file for extraction guidelines:
- `<skill-dir>/references/ingest-pdf.md` for path or zotero type
- `<skill-dir>/references/ingest-repo.md` for repo type
- `<skill-dir>/references/ingest-url.md` for url type

Follow its instructions for reading strategy, slug derivation, citekey
format, and article structure.

## Step 4: Determine slug and check for existing note

Before full extraction, derive the slug and citekey from the source metadata
(title, authors, repo name — see the reference guide for format).

- **slug** — kebab-case identifier for the note
- **citekey** — `path%...`, `zotero%...`, `repo%...`, or `url%...`

For zotero type, use `zotero%<citekey>` as the citekey (not `path%`).

Check if `$OBSIDIAN_KB_VAULT/<slug>.md` already exists. If it does, read it to understand
what's already captured — the extraction in Step 5 should incorporate with
the existing content rather than duplicate it.

## Step 5: Extract knowledge and write the note

Read the source material and produce the **article body** in markdown.

If a focus hint was provided, use it to scope the extraction — read only the
relevant sections, prioritize the specified topics, or skip what the user
asked to skip.

**If the note does not exist** — write the full article:

```bash
python3 <skill-dir>/scripts/create-note.py "<slug>" \
  --body-file /tmp/kb-body-<slug>.md \
  --citekey "<citekey>"
```

**If the note already exists** — merge with it using the available edit tool.
Add new sections, deepen existing ones, preserve what's already there.
This is common when re-ingesting with a different focus (e.g., first
ingestion covered chapters 1-3, now adding chapter 4).

## Step 6: Evolve the corpus

1. **Find related notes** — use `kb-search` (`similar` mode) to find notes
   related to the new slug. Read the top matches directly from the vault.

2. **Add links** — add `[[wikilinks]]` in the new note where it references
   concepts covered by existing notes. Only add a link back from an existing
   note if it genuinely references this one.

3. **Deduplicate concepts** — if the new note defines something already defined
   in another note, consider extracting the shared concept into its own note
   (merge definitions, note notation/framing differences, wikilink from originals).

4. **Split if needed** — if any note exceeds ~250 lines, split it into coherent
   pieces using `create-note.py` for the extracted parts.

## Step 7: Report

Tell the user:
- The slug and title of the note created
- Which existing notes were linked to/from
- Any shared concepts extracted or notes split

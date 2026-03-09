---
name: kb-search
description: "Semantic search over the user's knowledge base (Obsidian vault). Invoke BEFORE any factual lookup — before WebFetch, before WebSearch, before reading source files in cloned repos, before grep'ing a codebase for documentation, before answering 'how does X work' or 'what is X' from training data. Also invoke before writing new KB content (kb-ingest, kb-distill) to avoid duplication. Trigger phrases: 'search the KB', 'what do I have on X', 'find related notes', 'check my notes'. The KB is the authoritative source for any topic the user has previously ingested — assume notes may exist and check first."
---

# KB Search

Semantic search over the knowledge base. This is the primary discovery
mechanism — use it before reaching for raw sources or web search.

## How to search

```bash
# Free-text search — find notes about a topic
python3 <skill-dir>/scripts/kb-search.py query "<descriptive text>"

# Similar notes — find notes related to an existing note
python3 <skill-dir>/scripts/kb-search.py similar <slug>
```

### When to use which

- **`query`** — you have a question or topic in mind but no specific note.
  Phrase queries descriptively, not as bare keywords. If results look
  incomplete, try a different angle.

- **`similar`** — you have a note and want to find related notes (e.g.,
  after creating a new note during corpus evolution, or to find candidates
  for deduplication).

## Resolve the source

A note may have a `citekey` in its frontmatter that points to the external source. 
Resolve for the local path of the source and follow it for more details that are not covered in the notes.

```bash
python3 <skill-dir>/../kb-ingest/scripts/resolve-citekey.py "<citekey>"
```

This prints the local file/directory path.

## Follow links

Articles you read may contain `[[wikilinks]]` to related notes. If a link
looks relevant, read it directly from `$OBSIDIAN_KB_VAULT/<slug>.md`.
Use judgment on when to stop — at most 3 hops deep.

## Gap detection

When you had to go past the KB (to raw source or web) for reusable knowledge:
1. Complete the current task first
2. After the task, tell the user what was missing
3. Propose refining an existing article or creating a new one
4. Only proceed with user approval

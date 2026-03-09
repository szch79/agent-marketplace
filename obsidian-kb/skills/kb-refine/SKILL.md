---
name: kb-refine
description: "Refine and deepen an existing knowledge base article by re-reading raw sources with a specific question in mind. Use when gap detection identified missing knowledge, or when the agent needs to deepen an article that was too shallow for the current task. Triggers for 'deepen this article', 'refine the KB on X', 'fill in this gap', 'the KB was too shallow on X'."
---

# KB Refinement

Deepen an existing article by re-reading the raw source with a specific
question — "what do I need, and what's missing?" Ingestion is coarse and
exploratory; refinement is targeted and purposeful. You already know what
gap to fill.

## Inputs

The refinement request includes:
- **Target article** — which KB note to deepen
- **The gap** — what specific knowledge was missing
- **Context** — what task revealed the gap

## Step 1: Read the current article

Read the article directly from the vault. Understand what's already captured
and where the gap is.

## Step 2: Resolve the citekey

If the article has a `citekey` in its frontmatter, resolve it to a local path:

```bash
python3 <skill-dir>/../kb-ingest/scripts/resolve-citekey.py "<citekey>"
```

This prints the local file/directory path. Then read the source using the
available read tool (use `pages` for PDFs when supported).

Focus narrowly on the gap — don't re-read the entire source. For PDFs, target
the specific pages/chapters. For repos, target the specific source files.

## Step 3: Update the article

Read the vault file directly and edit it with the available edit tool to deepen the
relevant section:

- Add new definitions, theorems, or results with page references (for PDFs)
- Add new data types, algorithms, or patterns with file paths (for repos)
- Add `[[wikilinks]]` where the text references concepts covered elsewhere

Keep the article under ~250 lines after the update.

## Step 4: Split if needed

When a note exceeds ~250 lines after editing:

1. Extract a coherent section into a new note:
   ```bash
   python3 <skill-dir>/../kb-ingest/scripts/create-note.py "<child-slug>" \
     --body-file /tmp/kb-body-<child-slug>.md \
     --citekey "<citekey>"
   ```
   If the extracted section covers the same source, give it the same citekey.

2. Replace the extracted section in the original with a `[[child-slug]]` wikilink.

3. Add `[[wikilinks]]` where the text references concepts covered elsewhere.

## Step 5: Report

Tell the user:
- What was deepened and how
- Any new notes created from splitting

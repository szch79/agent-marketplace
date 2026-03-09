---
name: kb-distill
description: "Distill KB-worthy knowledge from the current conversation — identifies concepts, connections, and insights worth preserving, then creates or updates notes in the vault. Use whenever the user says 'distill the KB', 'extract knowledge from this conversation', 'what did we learn', or invokes /kb-distill or $kb-distill. Also triggers for 'save what we figured out', 'add our findings to KB', or 'capture these insights'."
disable-model-invocation: true
---

# KB Distill

Extract reusable knowledge from the current conversation and integrate it into
the KB. Unlike ingestion (which processes external sources), kb-distill mines
the conversation itself — the thinking, discoveries, and connections that
emerged during work.

## Input

This skill runs in the main context — it needs the full conversation history.
The user may optionally provide hints via $ARGUMENTS (e.g., a focus area or
specific insight to capture).

## Procedure

### 1. Mine the conversation

Review the conversation and identify KB-worthy pieces. Look for:
- **Concepts** — techniques, systems, or ideas that were defined or clarified
- **Connections** — relationships discovered between existing KB topics
- **Insights** — patterns, tradeoffs, or practical lessons learned through work

Filter ruthlessly. Only extract knowledge that is:
- Reusable across future sessions (not one-off debugging)
- Distilled enough to be evergreen (not "we tried X and it failed")
- Not already captured in existing KB articles

### 2. Check existing KB

For each candidate piece, use `kb-search` (`query` mode) to find related notes.
Read the top matches.

Classify each piece as:
- **Update** — an existing article covers this topic → update it directly
- **New** — no existing article covers this topic → create a new note
- **Skip** — already adequately covered

### 3. Propose to user

Present the proposals as a list:

```
I found N pieces of KB-worthy knowledge in our conversation:

1. [NEW] "sdd-vtree-balancing-tradeoffs" — Balancing vtree depth vs apply performance
   (related to [[darwiche-sdd]])
2. [UPDATE "[[lean4-elaboration]]"] — Add section on do-notation desugaring edge cases
3. [NEW] "rust-trait-object-perf" — When trait objects beat generics for binary size
```

Wait for user approval. The user may approve all, select specific items, or
modify proposals.

### 4. Create or update notes

For each approved item:

**New notes:**
1. Write the article body to `/tmp/kb-body-<slug>.md` using the available write tool.
2. Create via:
   ```bash
   python3 <skill-dir>/../kb-ingest/scripts/create-note.py "<slug>" \
     --body-file /tmp/kb-body-<slug>.md
   ```
   Distilled notes have no citekey (no external source).
3. **Evolve**: use `kb-search` (`similar` mode) to find related notes,
   add `[[wikilinks]]` where the text naturally references
   other concepts. Check for concept
   overlap — if the new note defines something already covered elsewhere,
   extract the shared concept into its own note. Split any note exceeding
   ~250 lines.

**Updates:**
Read the vault file and use the available edit tool. Add `[[wikilinks]]` where the text
references other concepts. Split if the note exceeds ~250 lines after the update.

### 5. Report

Tell the user what was created/updated and which notes were linked.

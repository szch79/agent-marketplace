# obsidian-kb

## Link semantics

A `[[wikilink]]` from A to B means A references a concept that B covers in
more detail. Add links where the reference is natural in the text — don't mirror links mechanically.

## Vault path

Notes live at `$OBSIDIAN_KB_VAULT/<slug>.md`. To get the path:
```bash
echo $OBSIDIAN_KB_VAULT
```

## Lookup Policy

**ALWAYS search the KB first** when you need information about a topic that
could plausibly have a note — before reading source code, clones, raw files,
or the web. Use `kb-search` to check. Only fall back to other sources if the
KB has no relevant results.

If you found a relevant note but still had to fall back to other sources to
get what you needed, the note needs refinement. After completing the task,
tell the user what was missing and propose refining the note.

## Resolve the source

A note may have a `citekey` in its frontmatter that points to the raw source. 
Resolve for the local path of the source and follow it for more details that are not covered in the notes.

```bash
python3 <skill-dir>/../kb-ingest/scripts/resolve-citekey.py "<citekey>"
```

This prints the local file/directory path.

## Formatting

Use MathJax for all mathematical notation.

- Inline math: `$...$`
- Display math: `$$...$$`
- Inference rules: use `\dfrac{premises}{conclusion}` in display math, not
  backtick code blocks
- Don't compress formal notation into code blocks — write it as proper math

## Corpus evolution

### Principles

- **Search before writing.** Before adding content, use `kb-search` to find
  related notes. Integrate, not duplicate.

- **Deduplicate concepts.** When something you're adding already exists in
  another note — even partially, even with different notation — don't create
  a parallel definition. Extract the shared concept into its own note, merge
  the perspectives, note any notation or framing differences, and wikilink
  from the originals.

- **Associated external source.** Notes with a `citekey` in frontmatter
  have an external source you can access. To resolve a citekey to a local path:
  ```bash
  python3 <plugin-dir>/skills/kb-ingest/scripts/resolve-citekey.py "<citekey>"
  ```

### Mechanics

- **Split at ~250 lines.** When a note exceeds ~250 lines, split it into
  coherent pieces. Each piece becomes its own note, linked from the original.
- **Don't hesitate to create multiple notes.** It is expected and encouraged.
- **Add Examples.** MVEs are encouraged as a distillation of critical technical details and programming patterns.

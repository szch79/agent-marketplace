# PDF Ingestion

## Reading strategy

Adapt to the source length:

- **Conference papers** (~10-30 pages): read linearly. Skip front matter
  (cover, copyright). Content is dense enough to read straight through.
- **Theses and books**: start from the TOC. Read chapter overviews and key
  results. Grep for definitions, theorems, lemmas to find the important
  parts. Don't read every section — a chapter summary often suffices.

For long PDFs, read in chunks using the available read tool's `pages` parameter when supported.

## Determine the slug and citekey

Derive a kebab-case slug from the first author's last name and a short
topic keyword:
- "SDD: A New Canonical Representation..." by Darwiche → `darwiche-sdd`
- "Attention Is All You Need" by Vaswani et al. → `vaswani-attention`

Citekey format: `path%<absolute-path-to-pdf>`

## Article body

The level 1 header should be the title of the article.

Write a KB article that captures the source's key contributions. Structure
should fit the source — use your judgment:

- **Summary** (1-3 sentences): what it introduces, why it matters, key claim
- **Core concepts**: key definitions and terms with page references `(p. N)` and theorem numbers.
- **Key results**: theorems, algorithms, main findings with page references
- For **books/theses**: organize by chapter or section instead

Use explanation lists for a list of definitions, theorems, etc; also include theorem numbers:

```markdown
- **<name>** (def. 1.2.3) :: explanation.
```

Page references like `(p. 42)` or `(Ch. 3, §2)` are critical — they let
the source be revisited during refinement.  

Keep under ~250 lines. For books, create a high-level overview; details
come later via kb-refine.

## Zotero sources

When the source type is `zotero`, the PDF path has already been resolved
(Step 2). The only differences:

- **Citekey format**: `zotero%<better-bibtex-citekey>`
- **Metadata**: title, authors, year are available from the citekey

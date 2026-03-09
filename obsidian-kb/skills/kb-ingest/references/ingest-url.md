# URL Ingestion

## Reading strategy

Determine scope from the URL and page content:

- **Single-page content** (blog post, paper page, article): fetch the URL
  with the available web fetch tool. Read the returned markdown in full. This is the
  conference-paper equivalent.

- **Documentation site** (official docs, multi-section reference):
  1. Fetch the entry URL. Extract navigation structure from links.
  2. If focus hint given, select matching sections only.
  3. Otherwise, read the overview/intro page, then pick 3-5 key pages.
  4. **Fetch each subpage** with the available web fetch tool to read its full content.
     Do not rely solely on the entry page — subpages contain the actual material.
  5. Cap at ~10 page fetches per ingestion.
  Deeper coverage comes later via kb-refine.

If a page fails to fetch or returns garbled content, skip it and note the
gap. Suggest the user provide a local copy if the site is unfetchable.

## Determine the slug and citekey

For articles, derive slug from author + topic (like PDFs):
- "A Complete Guide to useEffect" by Dan Abramov → `abramov-useeffect`
- "Thinking in React" on react.dev → `react-thinking-in-react`

For documentation, derive slug from the project/library name:
- https://react.dev/learn/hooks → `react-hooks-docs`
- https://docs.python.org/3/library/ → `python-stdlib-docs`

Citekey format: `url%<canonical-url>` (strip tracking params and fragments).

## Article body

The level 1 header should be the title of the article or documentation.

### For articles (single page)

Same structure as PDF articles:
- **Summary** (1-3 sentences): what it covers, key insight
- **Core concepts**: definitions, key ideas with section references `(§ Section Name)`
- **Key points**: arguments, findings, recommendations

### For documentation sites

Orient the reader, don't exhaustively document:
- **Summary**: what this documentation covers, target audience
- **Key concepts**: central abstractions, important terms
- **Section map**: overview of doc structure (like Module Atlas in repo notes)
- **Key pages**: most important pages with one-line descriptions

Keep under ~250 lines. Create separate notes for major subsections only if
the content warrants it.

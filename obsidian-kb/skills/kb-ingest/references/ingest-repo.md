# Repo Ingestion

## Locate the repository

The repo has already been cloned (Step 2) to `ZOB_assets/repos/<name>/`. Derive the repo name from the directory name.

## Explore the repository

Read and analyze:
- README and documentation
- Directory structure and module layout
- Key source files (entry points, core modules)
- Core definitions: data types, structures, modules/type class/traits etc.
- Core algorithms and their purpose
- Language(s) and framework(s) used

## Determine the slug and citekey

Use the repo name as the slug (e.g., `oxidd`, `lean4-mathlib`, `tokio`).

Citekey format: `repo%<repo-name>`

## Article structure

Adapt based on the source — not all sections required:

```markdown
# <Repo Name>

One-line description. Language: <lang>. Related: [[existing-article]].

## Architecture

High-level architecture summary. Intentionally vague — just enough to orient.

## Core Definitions

- **<TypeName>** :: what it represents, where defined (`src/core/types.ts`)

## Core Algorithms

- **<Algorithm>** :: what it does and why (`src/search.js:L42-L80`)

## Module Atlas

| Directory | Purpose |
|-----------|---------|
| `src/core/` | Core logic |
| `src/utils/` | Shared utilities |

## Key Files

- `src/main.ts` :: entry point

## Relations

- [[related-article]] :: how this repo relates
```

Guidelines:
- Keep under ~250 lines. For large repos, stay high-level.
- Use file paths relative to repo root.
- Focus on what's essential to understand the repo, not exhaustive documentation.

## Large repos: keep it high-level

For repos with multiple distinct subsystems, keep the overview article high-level. Mention subsystems in prose or in the Architecture section, but only create `- [[slug]] :: one-liner` entries for aspects you actually document as separate notes during this ingestion. Additional aspects get documented later via the refinement skill when real work needs them.

Skip sub-articles if the repo is small enough that everything fits in the overview.

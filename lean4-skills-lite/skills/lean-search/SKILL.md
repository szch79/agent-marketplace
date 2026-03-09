---
name: lean-search
description: "Search Lean 4 libraries (Mathlib, Init, Std, Batteries) for lemmas, theorems, definitions, type classes, notation, and tactics. Invoke BEFORE guessing any Lean/Mathlib name, grep'ing a local mathlib clone, reading mathlib source files, or WebFetch'ing leanprover-community pages. Also invoke when picking premises for simp/aesop/grind, when checking if a lemma exists, or when looking up the canonical name of a known concept. Trigger phrases: 'does mathlib have', 'find lemma', 'what theorem', 'search mathlib', 'is there a lemma for'. Also triggers on loogle query syntax like '?a -> ?b' and on Lean goal text starting with '⊢'. Mathlib is large and naming is non-obvious — assume the lemma exists and search first."
disable-model-invocation: false
---

# Lean Library Search

## Which tool to use

- **Natural language** ("sum of two primes", "commutativity of addition") — **semantic** (queries leansearch)
- **Type pattern** (`?a → ?b → List ?a`) — **loogle**
- **Have Lean goal text** (`⊢ |re z| ≤ ‖z‖`) — **leanfinder** (only for `⊢` goals or Lean expressions; returns null names for plain English)
- **Have goal, want closing lemmas** — **state_search**
- **Want premises for `simp`/`aesop`/`grind`** — **hammer_premise**

## Usage

```bash
python3 <skill-path>/scripts/search.py <api> "<query>"
```

Examples:
```bash
python3 <skill-path>/scripts/search.py semantic "sum of two even numbers is even"
python3 <skill-path>/scripts/search.py loogle "(?a → ?b) → List ?a → List ?b"
python3 <skill-path>/scripts/search.py leanfinder "⊢ |re z| ≤ ‖z‖"
python3 <skill-path>/scripts/search.py state_search "⊢ n + m = m + n"
python3 <skill-path>/scripts/search.py hammer_premise "⊢ n + m = m + n"
```

Use returned names from state_search/hammer_premise with: `simp only [name1, name2]`, `aesop`, or `grind [name1, name2]`.

## Loogle query syntax

- `(?a → ?b) → List ?a → List ?b` — type shape
- `Real.sin` — by constant name
- `_ * (_ ^ _)` — subexpression wildcard
- `|- _ + 0 = _` — search by conclusion only
- `"comm"` — name substring match

## Rate limits

| API | Limit |
|-----|-------|
| semantic | 3 / 30s |
| loogle | 3 / 30s |
| leanfinder | 10 / 30s |
| state_search | 6 / 30s |
| hammer_premise | 6 / 30s |

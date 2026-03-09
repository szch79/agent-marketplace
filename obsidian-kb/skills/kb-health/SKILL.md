---
name: kb-health
description: "Check knowledge base vault consistency — finds orphan notes and oversized articles. Use whenever the user says 'check KB health', 'audit the vault', or invokes /kb-health. Also triggers for 'are there any KB issues', 'vault consistency', or 'find orphan notes'."
---

# KB Health Check

Run consistency checks on the Obsidian knowledge base vault and report issues.

## Procedure

### 1. Run the health check script

```bash
python3 <skill-dir>/scripts/health-check.py
```

This outputs a JSON report with two arrays:
- `orphans` — note slugs not linked from any other note
- `oversized` — `{file, lines}` entries for notes exceeding 250 lines

### 2. Propose fixes

For each issue category, propose fixes to the user:
- Orphans → use `kb-search` to find related notes and suggest where to add links
- Oversized → split candidates (read the note and suggest which section to extract)

Only act on fixes the user approves.

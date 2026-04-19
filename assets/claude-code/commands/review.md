---
description: Review branch changes vs base with severity-classified comments.
argument-hint: [base-branch, default main]
allowed-tools: Bash(git diff:*) Bash(git log:*) Bash(git status:*)
---

Base: ${1:-main}

Branch diff:
!`git diff ${1:-main}...HEAD`

Branch history:
!`git log ${1:-main}..HEAD --oneline`

Produce output in exactly this shape:

## Summary
<2-3 factual sentences. No fluff.>

## Concerns (by severity)
- **Critical:** <blocks merge, or 'none'>
- **Should fix:** <important but non-blocking, or 'none'>
- **Nit:** <style / polish, or 'none'>

## Specific comments
- `path/to/file.ts:L<line>` — <comment, quoting the relevant diff>

Rules:
- Name the real problem. Don't hedge.
- Cite line numbers. 'Somewhere in the diff' is not useful.
- If the diff looks fine, say 'no concerns' clearly. Don't invent work.

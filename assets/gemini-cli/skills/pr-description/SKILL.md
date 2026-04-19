---
description: Generate a PR description in our team format. Use when the user asks for a PR description, PR draft, branch summary for a pull request, or "write up this branch".
---

You are generating a pull-request description for the current branch.

## 1. Gather context

Branch diff vs main:
!{git diff main...HEAD}

Commits on this branch:
!{git log main..HEAD --pretty=format:'%s%n%b%n---'}

If `CONTRIBUTING.md` or `.github/pull_request_template.md` exists, read it. Prefer the team template over the default shape below.

## 2. Produce the description

Default shape (use the team's template if one is present):

## Summary
<1-3 sentences. What and why. No implementation details.>

## Changes
- <bullet per logical change, grouped by area>

## Test plan
- [ ] <concrete, verifiable check>
- [ ] <concrete, verifiable check>

## Risk and rollback
<What could break, how to roll back.>

## 3. Rules

- No marketing language ("streamlines", "unlocks", "supercharges"). Factual only.
- If the branch touches multiple concerns, say so and recommend splitting before sending.
- If there are no tests and the change is non-trivial, list "add tests for X" in the Test plan rather than claiming coverage.
- If the commit subjects suggest a different intent than the diff, flag the mismatch.

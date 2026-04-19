---
description: Inspect staged changes and commit with a conventional-commit message.
allowed-tools: Bash(git diff:*) Bash(git status:*) Bash(git log:*) Bash(git commit:*)
---

## Context

Status:
!`git status --short`

Staged diff:
!`git diff --staged`

Recent commit style:
!`git log --pretty=format:'%s' -10`

## Task

Produce a conventional-commit message matching the style above.

Rules:
- Subject under 72 chars, imperative mood, no trailing period.
- Body explains the *why*. The diff already shows the what.
- If the diff mixes unrelated concerns, propose a split instead of committing.
- If the diff is empty, tell me and stop.

Once the message is correct, run:
```!
git commit -m "<subject>" -m "<body>"
```

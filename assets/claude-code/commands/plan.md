---
description: Produce an implementation plan for a task without writing any code.
argument-hint: [task description]
allowed-tools: Read Grep Glob
disable-model-invocation: false
---

You are planning (not executing) the following task:

**$ARGUMENTS**

Before producing the plan:
1. Skim the repo to locate the most relevant files (Grep/Glob). Do not read more than 5 files in full — read narrowly.
2. Note any conventions from CLAUDE.md that apply.

Produce a plan in this shape:

## Goal
<1-2 sentences, concrete and verifiable>

## Scope
- **Will touch:** <files>
- **Will not touch:** <files / areas explicitly out of scope>

## Changes (ordered)
1. `path/to/file.ts` — <what changes, why>
2. `path/to/other.ts` — <what changes, why>

## Verification
- <concrete command or check that tells us we succeeded>

## Risks
- <anything that could break unexpectedly>

## Open questions
- <things I need you to decide before I can proceed>

Do NOT edit anything. Stop after the plan.

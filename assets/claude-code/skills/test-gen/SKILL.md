---
description: Generate tests for a specific function or module. Use when the user asks to write tests, add coverage, or test a particular file/function.
argument-hint: [file-or-function]
allowed-tools: Read Grep Glob Edit Write Bash(pnpm test:*) Bash(npm test:*) Bash(jest:*) Bash(vitest:*) Bash(pytest:*)
---

You are generating tests for: **$ARGUMENTS**

## 1. Read first, don't guess

- Read the target file in full.
- Grep for existing tests of this file (`**/*.test.*`, `__tests__/**`, `test/**`, etc.). Match the existing test style — framework, assertion library, fixtures.
- If there are no nearby tests, skim one or two test files elsewhere in the repo to learn the conventions.

## 2. Design the tests before writing them

Output the test plan first, *before* writing any test code:

## Test plan
- **Happy path:** <describe>
- **Input boundaries:** <empty, max length, unicode, etc. — only those that matter for this function>
- **Error paths:** <throwable or Result-returning conditions, based on what you actually read in the code>
- **Interactions:** <mocks only for external IO; prefer real objects for internal collaborators>

Pause for my approval before writing the tests. If I skip approval, proceed but minimize.

## 3. Write the tests

- Match the existing naming and organization. If the repo uses `describe/it` blocks, so do you. If it uses function-level tests, same.
- One assertion per logical check. Don't smuggle multiple behaviors into one `it` block.
- Use real inputs. Don't mock the thing under test; mock only its external collaborators.
- If a test requires setup > 5 lines, factor it into a helper. Don't inline 20-line setup blocks.

## 4. Run the tests

After writing, run just the new test file. Show me the output.

If any new test fails, stop. Don't "fix" by softening the assertion — the failing test is often revealing a real bug in the target. Ask me before changing production code.

# Chapter 16 — Test Generation and Automation

> The failure mode of AI-assisted testing is tests that pass while the feature is broken. This chapter is about avoiding that specifically.

---

## The concept

Letting an agent generate tests is the most obvious productivity win in the category. It's also the most common source of *false confidence* — tests that compile, run, pass, and tell you nothing about whether the feature actually works.

Durable truth: **tests are only useful if they can fail when the code is wrong.** An agent that doesn't internalize this will produce tests that are essentially elaborate tautologies ("given what the code does, assert it does it"). You have to brief for it.

## The two failure modes to avoid

### 1. Test-the-implementation

The agent reads the code and writes tests that assert the exact branches it just saw. If you change the implementation, the tests break even when the behavior is correct. These tests don't buy you anything — they're coupled to the code, not the contract.

### 2. Test-the-happy-path-only

Tests pass with pristine inputs. Real bugs hide at boundaries — empty strings, max length, unicode, nulls, concurrent calls, permission denied, timeouts. An agent left to its own devices picks the sunny path 80% of the time.

Both failure modes are *prompt-able*. See below.

## The durable briefing shape for test generation

When you ask an agent to generate tests, make sure the brief forces:

1. **Tests from the contract, not the implementation.** "Write tests against the public behavior described in <doc/interface/spec>. Do not refer to the implementation when choosing test cases."
2. **An explicit plan before code.** "Produce the test plan first. What happy paths, what boundaries, what error paths, what interactions? Pause for my approval."
3. **Match the existing style.** Read nearby tests. Use the same framework, assertion library, fixture shape, naming convention.
4. **Minimize mocks.** Mock external I/O only. For internal collaborators, prefer real objects.
5. **Run the tests** at the end. Show the output. If anything fails, *stop* — don't soften the test to pass.

The [`test-gen` skill in assets](../../assets/claude-code/skills/test-gen/) encodes exactly this discipline. Use it, or paste its body into a command of your own.

## The three kinds of tests to generate

### Unit

Small, fast, narrow. An agent is great at these. Brief: give it the function, ask for happy path + 2-3 meaningful boundaries + 1-2 error paths. Demand the function's public signature; forbid reading the internals beyond what's necessary.

### Integration

Slower, broader, involves real(ish) collaborators. Agent still useful; brief more carefully. Name the collaborators that should be real (DB, queue, HTTP client to an in-process fake) vs mocked (payment provider, cloud vendor in unit-ish tests).

### End-to-end

The agent can generate these, but the framing matters: "simulate the user's happy path, not every branch." E2E tests are expensive; cover the paths that would make you panic if they broke, not every corner.

## In-loop test running

The biggest productivity unlock is letting the agent *run* tests during implementation, not just write them.

The pattern:

1. Agent makes a small change.
2. `PostToolUse` hook (or the agent's own habit) runs the relevant tests.
3. On failure, the error lands in the agent's context.
4. Agent self-corrects. Or, on a pattern it can't resolve, surfaces to you with the error.

Both tools support this via hooks (Ch. 8). Gate on specific paths (`paths: src/billing/**` in a skill's frontmatter) so you don't run the whole suite on every edit — that's slow and expensive.

## Test commands worth having

- **`/test <file-or-pattern>`** — a slash command that figures out the right test invocation for the repo and runs only what matches. Replaces "what's the test command for this repo" conversations.
- **`/test-gen <file>`** — wrapper around the `test-gen` skill for one-shot generation.
- **`/test-diag <failure>`** — given a failing test, diagnose why. Reads the test, reads the target, reads any recent changes via git.

Example `/test` command (TOML, Gemini CLI):

```toml
description = "Run tests for a specific path or filter."

prompt = """
Run tests matching: {{args}}

Start by detecting the test runner from the repo:
- If there's a `pnpm test` script, use it with the appropriate filter flag.
- If there's `jest`, `vitest`, `pytest`, `go test`, `cargo test`, pick the right one.

After running, summarize: passed, failed, errors. For failures, quote the
relevant assertion and the file:line that failed. Do not reinterpret the error.
"""
```

## Pitfalls specific to AI-generated tests

### Flaky tests masquerading as passing

An agent sometimes writes a test that happens to pass by accident (wrong assertion but right outcome). Catch these by running the test with the production code mutated (or just ask the agent to "intentionally break the production code and confirm the tests fail").

### Assertion drift

Over time, agents "fix" broken tests by loosening assertions. Put a hook on test files (or, better, a PR review policy) that surfaces assertion changes for human review.

### Over-testing uninteresting things

Every function gets three tests because "coverage." You end up with 400 tests where 100 would do, and the noise hides the signal.

Rule: if you can't explain why a test exists in one sentence, it probably shouldn't.

## Property-based testing

Where it applies, nothing beats it for agent-generated tests. The agent defines properties ("for any valid input, the result should satisfy P") and the property engine generates thousands of examples. Python (`hypothesis`), Rust (`proptest`), TS (`fast-check`). Try it for anything numeric, parsing, or serialization.

## Observability in test runs

When the agent's running tests in a loop:

- **Hook into PostToolUse on the test command** to append a line to an audit log: pass/fail counts, time elapsed, which tests ran.
- **Cap iterations.** The agent should stop after N failed test runs and surface, not infinitely retry.
- **Cache test outcomes where safe.** Running the full suite every turn is expensive; running only tests relevant to changed files is usually enough.

## References

- Test-gen skill asset — [`assets/claude-code/skills/test-gen/`](../../assets/claude-code/skills/test-gen/)
- Claude Code best practices — [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

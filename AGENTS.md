# AGENTS.md — The AI Coding Playbook

Memory file for both Claude Code and Gemini CLI, and any other agent that respects the emerging [AGENTS.md convention](https://agentskills.io). Both CLIs' contextFileName setting should include this file.

## What this repo is

A durable, opinionated guide to agentic coding — concepts first, tool-specific recipes second — covering Gemini CLI (primary), Claude Code (secondary), Google Antigravity, Stitch, Firebase Studio, Vertex AI Model Garden, Claude Agent SDK, and Google ADK. 21 chapters in `chapters/`, drop-in assets in `assets/`.

## How it's organized

- `README.md` — landing page, navigation.
- `docs/TABLE_OF_CONTENTS.md` — full TOC.
- `chapters/NN-name/README.md` — one concept chapter per directory.
- `chapters/NN-name/gemini-cli/` and `chapters/NN-name/claude-code/` — tool-specific realizations where relevant.
- `assets/gemini-cli/` and `assets/claude-code/` — runnable commands, skills, hooks, MCP configs, and settings examples, mirrored across both tools.
- `CHANGELOG.md` — what changed.
- `docs/GLOSSARY.md`, `docs/FAQ.md`, `docs/ROADMAP.md` — reference material.

## Writing conventions

- Second person ("you do this"), present tense.
- Opinionated. Where one approach is better, say so. Where it depends, say what it depends on.
- **No marketing language.** "Streamlines", "unlocks", "supercharges", "revolutionizes" are banned. Factual.
- Short paragraphs. Split at five sentences.
- Inline code with backticks. Block quotes for file content.
- Every tool/doc reference links to the primary source.
- Every chapter ends with a "What's next" pointing to related chapters.

## Commit conventions

- Author: `Vikas Mishra <vikvikvik007@gmail.com>` (configured locally for this repo).
- Commit message: subject under 72 chars, imperative, no trailing period. Body explains the *why* — the diff shows the what.
- One logical change per commit. Chapter concept in its own commit; each tool-specific realization in its own commit; each asset batch in its own commit.
- **No "Co-Authored-By" footer.** Commits are attributed to Vikas Mishra, not to any AI assistant.

## Durability principle

Concepts stay; realizations get updated when tools change. When writing a new chapter, separate the concept (the thing that's still true in three years) from the realization (the current API / filename / flag). Put the concept in `chapters/NN-name/README.md`; put realizations in `gemini-cli/` or `claude-code/` subdirs.

## What belongs in this repo

- Chapters explaining durable concepts.
- Runnable, tested, drop-in assets.
- Field reports (case studies of real usage) when contributed.
- Corrections to existing content with sourcing.

## What doesn't

- Marketing copy.
- AI-generated filler. If the agent wrote a section, it needs human editing before committing.
- Speculative chapters on tools that don't exist yet.
- Comparison matrices. (They age in weeks; the chapter-by-chapter framing ages better.)

## Test / build

This repo is documentation + shell scripts. There is no build step. Smoke test commands:

```bash
# Verify every hook script runs with a test payload and returns cleanly
for h in assets/*/hooks/*.sh; do
  echo "$h"
  echo '{"tool_input":{"command":"ls"}}' | "$h"
done

# Verify TOML parses for Gemini commands
for t in assets/gemini-cli/commands/*.toml; do
  python3 -c "import tomllib; tomllib.loads(open('$t').read())" && echo "ok: $t"
done

# Verify YAML frontmatter in skills
for s in assets/claude-code/skills/*/SKILL.md; do
  head -50 "$s" | grep -q '^---' && echo "ok: $s"
done
```

## Known traps

- Don't re-order chapters without updating `docs/TABLE_OF_CONTENTS.md` and the "What's next" links at the bottom of adjacent chapters.
- Don't promote the `chapters/NN/README.md` content by removing the `gemini-cli/` or `claude-code/` subdirs. The split is load-bearing for cross-chapter linking and for future-proofing.
- All absolute tool URLs go stale. Prefer `https://geminicli.com/docs/…` and `https://code.claude.com/docs/…` as the canonical roots; update aggressively when they change.

## References

- The playbook's own TOC: `docs/TABLE_OF_CONTENTS.md`
- Contributing guide: `CONTRIBUTING.md`
- Roadmap: `docs/ROADMAP.md`

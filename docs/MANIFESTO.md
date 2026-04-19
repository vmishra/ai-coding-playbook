# Manifesto

Why this repo exists, what it's trying to be, and — equally important — what it isn't.

## The problem this solves

The agentic coding space moves faster than anyone can document. Tools ship breaking changes quarterly. Blog posts written in spring are obsolete by autumn. Vendors publish setup guides but not judgment.

Most content is: a marketing page, a three-minute demo that doesn't survive a real codebase, or a tutorial that's six months stale. None of those survive actual work.

This playbook is designed to age well. Every chapter is organized around a **durable concept** — something that was true in 2023, is true now, and will still be true when today's CLIs are footnotes. The tool-specific sections are the *realization* of those concepts, not the substance.

Memory is a concept; `GEMINI.md` is a realization. Context hygiene is a concept; prompt caching and compaction are realizations. When tools change, the concept chapters stay; the recipes get updated.

The assets — slash commands, skills, MCP configs, hooks — are built to be cloned, customized, and kept.

## The Google-first stance

**Primary: [Gemini CLI](https://github.com/google-gemini/gemini-cli).** Open source, ships from Google, integrates cleanly with Vertex AI, Cloud Workstations, Firebase Studio, Stitch, and the rest of the Google developer stack. The right default if your tooling needs to compose with a Google cloud footprint.

**Secondary: [Claude Code](https://www.anthropic.com/claude-code).** Included because its abstractions — skills, subagents, hook events, permissions — are currently the most mature in the category, and the concepts generalize. If you understand Claude Code's hook model, you understand hooks in general.

This isn't a neutral comparison repo. Where one tool is clearly better for a task, it says so. Where the answer is "it depends," it says what it depends on.

## Who this is for

Working software engineers. You know what a shell is, you've shipped code, you've debugged something at 2 AM. You don't need "what is the terminal" or "save your file before running it."

If you've never written code, start with a language fundamentals course and come back when you have something to build.

## Who this isn't for

- People looking for a comparison spreadsheet. Those go stale in weeks.
- People looking for validation that their current stack is optimal. It probably isn't; nobody's is.
- People who want someone else to decide for them. This repo has opinions; you're supposed to push back on the ones you disagree with.
- Teams looking for a vendor-certified path. This is independent and stays that way.

## How this stays fresh

Two mechanisms.

**The concept / realization split.** Concept chapters describe invariants ("you need a way to give the agent durable context"). Realization sections describe the current tool-specific way to do that, and get updated when vendors change things.

**Versioned tags.** Every major tool-behavior claim references the version I tested. When a claim breaks, someone files an issue; the fix lands; the [CHANGELOG](../CHANGELOG.md) records it.

If you hit something that no longer works, open an issue with the tool version. That's the whole contract.

## On style

This guide is written by a human with opinions.

The two failure modes I've tried hardest to avoid: the breathless "unlock the power of" tone, and the hedged "there are many ways to approach this" non-answer. If you find either of those in here, file a bug.

Where I think one approach is clearly better than another, I say so and explain why. Where I'm genuinely unsure, I say that too. The whole thing is meant to be argued with.

## What "world-class" means here

Not: comprehensive coverage of every tool that exists.
Not: neutral, reference-style prose.
Not: up-to-the-hour on every release.

**Yes:** every claim sourced to primary docs, every asset runnable, every chapter opinionated enough to be useful six months from now, every piece of advice grounded in actual usage on actual codebases.

If you read this and feel like you're getting someone's hard-won judgment compressed into something you could finish in a weekend — that's the goal.

## The explicit non-goals

- **A comprehensive tool comparison matrix.** They go stale in weeks and become a maintenance tax. Chapter 2 is deliberately short.
- **Chasing every new product.** If it's not measurably different from something already covered, it doesn't get a chapter just for being new.
- **Vendor-specific certifications or partnerships.** This stays independent.
- **Tutorials for beginners who haven't shipped code.** Wrong audience.
- **YouTube-style "you won't believe" content.** No.

## If this resonates

Star the repo. Fork the repo. Break the repo's claims and file issues. Contribute assets. Write field reports — real case studies from real codebases — as issues with the `field-report` label. The most valuable signal this repo can receive is "I tried X from Chapter Y on a real thing; here's what happened."

If it doesn't resonate, that's okay too. There's no shortage of alternatives. Find the one that fits your brain.

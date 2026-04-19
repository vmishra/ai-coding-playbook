# FAQ

## Is this for Gemini CLI or Claude Code?

Both. Every concept chapter is tool-neutral; every realization section has Gemini CLI first, Claude Code second. If you're only using one, skip the other's section.

## Why Gemini CLI as primary?

It's open source, it's Google's canonical developer CLI, and it integrates natively with Vertex AI, Cloud Workstations, Firebase, Stitch, and the rest of the Google developer stack. If you're working in or near Google Cloud, it's the shortest path. If you aren't, Claude Code is an excellent second choice.

## Why do you keep mentioning "concepts" vs "realizations"?

Because the concepts — memory, context discipline, tool use, hooks, subagents — have been stable for three years and will probably still be stable in three more. The *realizations* — the specific commands, file formats, flags — change constantly. Organizing by concept means the playbook doesn't go stale every time a vendor ships a release.

## Do I need to read it in order?

No. See the recommended paths in the [README](../README.md). The chapters assume a little context from earlier ones, but each one is largely self-contained.

## What about Cursor / Copilot / Aider / Cline / Windsurf?

Cursor and Copilot are mentioned in Ch. 2 and Ch. 14 but not covered deeply — they're primarily IDE integrations, and the concepts transfer from the CLI chapters. Aider, Cline, and Windsurf are mentioned where relevant, mostly in Ch. 18 (local models).

## The tool changed since this was written. What do I do?

Open an issue with the version and what broke. The concept chapter is probably still correct; the realization section needs updating, and PRs are welcome. In the meantime, trust the concept and read the tool's latest official docs for current syntax.

## Is there a paid version / course?

No. MIT licensed. If you want to build a course on top of it, go ahead — that's why the license is permissive.

## Why isn't there a chapter on prompt engineering tricks?

Because most "tricks" don't survive model upgrades. The durable skill is framing tasks clearly and managing context; that's Ch. 3 and Part IV. If you want the latest jailbreak, this isn't the right book.

## How often does it update?

When something changes that meaningfully affects how you should do your work. Not on a calendar. Watch the repo or the CHANGELOG.

## I disagree with one of your recommendations.

Good. Open an issue with the reasoning. The point of an opinionated guide is that the opinions are visible and can be challenged.
